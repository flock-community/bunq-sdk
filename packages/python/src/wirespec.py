import json
import logging
from asyncio import Lock
from dataclasses import replace
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Dict, List, Optional

from api.Client import Client
from api.wirespec import Wirespec
from context import Context, refresh_session
from transport import Serialization, require_typed, send

logger = logging.getLogger(__name__)

SESSION_REJECTION = "Insufficient authentication."


def _authentication_headers(context: Context) -> Dict[str, List[str]]:
    config = context.config
    headers = {
        "X-Bunq-Client-Authentication": context.session_token,
        "Cache-Control": config.cache_control,
        "X-Bunq-Language": config.language,
        "X-Bunq-Region": config.region,
        "X-Bunq-Client-Request-Id": config.client_request_id,
        "X-Bunq-Geolocation": config.geolocation,
    }
    return {key: [value] for key, value in headers.items() if value}


def _is_session_rejected(response: Wirespec.RawResponse) -> bool:
    """bunq answers a dead session with 403 and this error description; other 403s are real permission errors."""
    if response.statusCode != 403 or not response.body:
        return False
    try:
        return any(error.get("error_description") == SESSION_REJECTION for error in json.loads(response.body)["Error"])
    except (ValueError, KeyError, TypeError, AttributeError):
        return False


# a session that expires within this many seconds is refreshed before the request is sent
EXPIRY_MARGIN = timedelta(seconds=30)


def transportation(
    context: Context,
    refresh: Callable[[Context], Awaitable[Context]] = refresh_session,
    on_context_change: Callable[[Context], None] = lambda context: None,
) -> Wirespec.Transportation:
    """
    Sends requests with the context's authentication headers.
    A session that has expired (or expires within 30 seconds) is refreshed before the request is sent.
    A 403 "Insufficient authentication." refreshes the session once (shared by concurrent requests) and retries the
    request with the new token. Statuses other than 200 and 400, including the original 403 when the refresh fails
    (a failed refresh before sending is not repeated after a 403 in the same request), are raised as BunqApiError.
    The refreshed context is kept inside this transportation, so later requests use the new token.
    on_context_change is called once with the new context after every successful refresh, so the caller can store it.
    """
    current = context
    lock = Lock()

    async def send_with(used: Context, request: Wirespec.RawRequest) -> Wirespec.RawResponse:
        headers = {**request.headers, **_authentication_headers(used)}
        return await send(used.config, replace(request, headers=headers))

    async def refreshed(used: Context) -> Optional[Context]:
        """Returns the refreshed context, or None when the refresh failed."""
        nonlocal current
        async with lock:
            # another request may have refreshed while this one waited; compared by identity because bunq returns the same session token on a re-created session
            if current is not used:
                return current
            try:
                new = await refresh(used)
            except Exception as e:
                logger.warning("bunq session refresh failed: %s", e)
                return None
            current = new
            on_context_change(new)
            return new

    class Transportation(Wirespec.Transportation):
        async def transport(self, request: Wirespec.RawRequest) -> Wirespec.RawResponse:
            snapshot = current
            # now() in the stored value's own time zone: naive values are compared with local time, aware ones with their zone
            # None when the refresh before sending failed: a 403 then does not trigger a second refresh in the same request
            pre_refreshed: Optional[Context] = snapshot
            if snapshot.session_expiry_time <= datetime.now(snapshot.session_expiry_time.tzinfo) + EXPIRY_MARGIN:
                pre_refreshed = await refreshed(snapshot)
            used = pre_refreshed or snapshot
            response = await send_with(used, request)
            if pre_refreshed is None or not _is_session_rejected(response):
                return require_typed(response)

            fresh = await refreshed(used)
            return require_typed(await send_with(fresh, request) if fresh else response)

    return Transportation()


def bunq_client(context: Context, on_context_change: Callable[[Context], None] = lambda context: None) -> Client:
    """
    Returns the generated async client, e.g. `await bunq_client(context).read_user(context.user_id)`.
    Sync callers can wrap a call in `asyncio.run(...)`.
    """
    return Client(Serialization(), transportation(context, refresh_session, on_context_change))

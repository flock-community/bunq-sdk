import json
import logging
from asyncio import CancelledError, Lock
from dataclasses import replace
from typing import Awaitable, Callable, Dict, List

from api.Client import Client
from api.wirespec import Wirespec
from context import Context, refresh_session
from transport import Serialization, send

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


def transportation(
    context: Context,
    refresh: Callable[[Context], Awaitable[Context]] = refresh_session,
) -> Wirespec.Transportation:
    """
    Sends requests with the context's authentication headers.
    A 403 "Insufficient authentication." refreshes the session once (shared by concurrent requests) and retries the
    request with the new token. Other responses, and the original 403 when the refresh fails, are returned as is.
    The refreshed context is kept inside this transportation, so later requests use the new token.
    """
    current = context
    lock = Lock()

    async def send_with(used: Context, request: Wirespec.RawRequest) -> Wirespec.RawResponse:
        headers = {**request.headers, **_authentication_headers(used)}
        return await send(used.config, replace(request, headers=headers))

    class Transportation(Wirespec.Transportation):
        async def transport(self, request: Wirespec.RawRequest) -> Wirespec.RawResponse:
            nonlocal current
            used = current
            response = await send_with(used, request)
            if not _is_session_rejected(response):
                return response

            async with lock:
                # another request may have refreshed the session while this one waited
                if current.session_token == used.session_token:
                    try:
                        current = await refresh(used)
                    except CancelledError:
                        raise
                    except Exception as e:
                        logger.warning("bunq session refresh failed: %s", e)
                        return response
                fresh = current
            return await send_with(fresh, request)

    return Transportation()


def bunq_client(context: Context) -> Client:
    """
    Returns the generated async client, e.g. `await bunq_client(context).read_user(context.user_id)`.
    Sync callers can wrap a call in `asyncio.run(...)`.
    """
    return Client(Serialization(), transportation(context))

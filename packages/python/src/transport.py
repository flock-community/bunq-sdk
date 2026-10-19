import builtins
import json
from dataclasses import asdict, is_dataclass
from functools import reduce
from typing import Any, Dict, List, Type, get_origin, get_args

import httpx
from dacite import from_dict

from api.wirespec import Wirespec, T
from signing import Signing


def _convert(raw: str, type: Any) -> Any:
    return int(raw) if type is int else raw


class Serialization(Wirespec.Serialization):

    def serializeBody(self, t: T, type: Type[T]) -> bytes:
        if t is None:
            return b""
        if is_dataclass(t) and not isinstance(t, builtins.type):
            return json.dumps(asdict(t)).encode('utf-8')
        raise Exception('Unsupported type')

    def deserializeBody(self, raw: bytes, type: Type[T]) -> Any:
        data = json.loads(raw)
        if "Response" not in data:
            if "Error" not in data:
                raise Exception("Invalid bunq response: neither Response nor Error")
            # error responses have no Response envelope: the whole document is the body
            return from_dict(data_class=type, data=data)

        res_data = data["Response"]
        if get_origin(type) is list:
            generic = get_args(type)[0]
            return [from_dict(data_class=generic, data=next(iter(it.values()))) for it in res_data]
        return from_dict(data_class=type, data=reduce(lambda acc, cur: {**acc, **cur}, res_data, {}))

    def serializePath(self, t: T, type: Type[T]) -> str:
        return str(t)

    def deserializePath(self, raw: str, type: Type[T]) -> T:
        return _convert(raw, type)

    def serializeParam(self, value: T, type: Type[T]) -> List[str]:
        return [] if value is None else [str(value)]

    def deserializeParam(self, values: List[str], type: Type[T]) -> T:
        return _convert(values[0], type)


async def send(config, raw_req: Wirespec.RawRequest) -> Wirespec.RawResponse:
    """Sends a signed request. Sync callers can use `asyncio.run(send(...))`."""
    headers = [(key, value) for key, values in raw_req.headers.items() for value in values if value.strip()]
    headers.append(('User-Agent', (config.user_agent or '').strip() or config.service_name))
    if raw_req.body is not None:
        headers.append(('X-Bunq-Client-Signature', Signing.sign_data(config, raw_req.body.decode('utf-8'))))

    # shortcut: one client per request, no connection reuse; share a client if throughput matters
    async with httpx.AsyncClient() as http:
        res = await http.request(
            method=raw_req.method,
            url=config.bunq_server.base_url + '/'.join(raw_req.path),
            params=[(key, value) for key, values in raw_req.queries.items() for value in values],
            headers=headers,
            content=raw_req.body)

    res_headers: Dict[str, List[str]] = {}
    for key, value in res.headers.multi_items():
        res_headers.setdefault(key.lower(), []).append(value)

    return Wirespec.RawResponse(res.status_code, res_headers, res.content)


class BunqApiError(Exception):
    """bunq (or a proxy in front of it) answered with something other than a 200 with a `Response` or a 400 with an `Error`."""

    def __init__(self, status: int, body: str):
        super().__init__(f"Received {status}: {body[:500]}")
        self.status = status
        self.body = body


def _is_object_with(body: bytes, key: str) -> bool:
    try:
        parsed = json.loads(body)
    except ValueError:
        return False
    return isinstance(parsed, dict) and key in parsed


def require_typed(response: Wirespec.RawResponse) -> Wirespec.RawResponse:
    """Only a 200 with a `Response` object or a 400 with an `Error` object is for the generated client; anything else is an error for the caller."""
    body = response.body or b""
    envelope = {200: "Response", 400: "Error"}.get(response.statusCode)
    if envelope and _is_object_with(body, envelope):
        return response
    raise BunqApiError(response.statusCode, body.decode('utf-8', 'replace'))


def require_signed(response: Wirespec.RawResponse, server_public_key: str) -> Wirespec.RawResponse:
    """Like require_typed, and the body must carry a valid `X-Bunq-Server-Signature` for the server public key."""
    require_typed(response)
    signature = next((values[0] for name, values in response.headers.items()
                      if name.lower() == "x-bunq-server-signature" and values), None)
    if not Signing.verify_response(server_public_key, response.body or b"", signature):
        raise Exception("Invalid bunq server signature")
    return response

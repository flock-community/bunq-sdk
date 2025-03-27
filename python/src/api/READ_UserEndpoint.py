from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .UserRead import UserRead
from .READ_User400ResponseBody import READ_User400ResponseBody

class READ_UserEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[None]):
    @dataclass
    class Path (Wirespec.Request.Path):
        itemId: int 
    @dataclass
    class Queries (Wirespec.Request.Queries): pass
    @dataclass
    class Headers (Wirespec.Request.Headers):
        CacheControl: Optional[str]
        UserAgent: str
        XBunqLanguage: Optional[str]
        XBunqRegion: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqGeolocation: Optional[str]
        XBunqClientAuthentication: str

    @property
    def body(self) -> None:
      return self._body

    @property
    def path(self) -> Path:
      return self._path

    @property
    def queries(self) -> Queries:
      return self._queries

    @property
    def headers(self) -> Headers:
      return self._headers

    method: Wirespec.Method = Wirespec.Method.GET

    def __init__(self, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str):
      self._path = READ_UserEndpoint.Request.Path(itemId = itemId)
      self._queries = READ_UserEndpoint.Request.Queries()
      self._headers = READ_UserEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self._body = None

  @staticmethod
  def to_raw_request(serialization: Wirespec.Serializer, request: Request) -> Wirespec.RawRequest:
    return Wirespec.RawRequest(
      path = ["user", str(request.path.itemId)],
      method = request.method.value,
      queries = {},
      headers = {
        "Cache-Control": serialization.serialize_param(request.headers.CacheControl, type(Optional[str])),
        "User-Agent": serialization.serialize_param(request.headers.UserAgent, type(str)),
        "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, type(Optional[str])),
        "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, type(Optional[str])),
        "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, type(Optional[str])),
        "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, type(Optional[str])),
        "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, type(str))},
      body = serialization.serialize(request.body, type(None)),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return READ_UserEndpoint.Request(
        itemId = serialization.deserialize(request.path[1], int),
  CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
  XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str)
  )

  @dataclass
  class Response200(Wirespec.Response[UserRead]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> UserRead:
      return self._body

    status: int = 200

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UserRead):
      self._headers = READ_UserEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  @dataclass
  class Response400(Wirespec.Response[READ_User400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> READ_User400ResponseBody:
      return self._body

    status: int = 400

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: READ_User400ResponseBody):
      self._headers = READ_UserEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case READ_UserEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {
            "X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, type(Optional[str])),
            "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, type(Optional[str])),
            "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, type(Optional[str]))},
          body = serialization.serialize(response.body, UserRead),
        )
      case READ_UserEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {
            "X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, type(Optional[str])),
            "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, type(Optional[str])),
            "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, type(Optional[str]))
          },
          body = serialization.serialize(response.body, READ_User400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return READ_UserEndpoint.Response200(
          body = serialization.deserialize(response.body, UserRead),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case 400:
        return READ_UserEndpoint.Response400(
          body = serialization.deserialize(response.body, READ_User400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def READ_User(self, req: Request) -> Response: pass

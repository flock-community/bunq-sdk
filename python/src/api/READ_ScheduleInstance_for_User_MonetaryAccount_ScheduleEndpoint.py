from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

from .ScheduleInstanceRead import ScheduleInstanceRead
from .READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody import READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody

class READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[None]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        scheduleID: int 
        itemId: int 
    @dataclass
    class Queries (Wirespec.Request.Queries): pass
    @dataclass
    class Headers (Wirespec.Request.Headers):
        CacheControl: 'Optional[str]'
        UserAgent: 'str'
        XBunqLanguage: 'Optional[str]'
        XBunqRegion: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqGeolocation: 'Optional[str]'
        XBunqClientAuthentication: 'str'
 
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

    _body:  None
    _headers: Headers
    _queries: Queries
    _path: Path
    method: Wirespec.Method = Wirespec.Method.GET

    def __init__(self, userID: int, monetaryaccountID: int, scheduleID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str):
      self._path = READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, scheduleID = scheduleID, itemId = itemId)
      self._queries = READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request.Queries()
      self._headers = READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self._body = None

  @dataclass
  class Response200(Wirespec.Response[ScheduleInstanceRead]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> ScheduleInstanceRead:
      return self._body

    _body: ScheduleInstanceRead
    _headers: Headers
    status: int = 200

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: ScheduleInstanceRead):
      self._headers = READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  @dataclass
  class Response400(Wirespec.Response[READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody:
      return self._body

    _body: READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody
    _headers: Headers
    status: int = 400

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody):
      self._headers = READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  Response = Response200 | Response400

  class Handler(Wirespec.Endpoint.Handler):
    @abstractmethod
    def READ_ScheduleInstance_for_User_MonetaryAccount_Schedule(self, req: 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request') -> 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response': pass

  class Convert(Wirespec.Endpoint.Convert[Request, Response]):
    @staticmethod
    def to_raw_request(serialization: Wirespec.Serializer, request: 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request') -> Wirespec.RawRequest:
      return Wirespec.RawRequest(
        path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetaryaccountID), "schedule", str(request.path.scheduleID), "schedule-instance", str(request.path.itemId)],
        method = request.method.value,
        queries = {},
        headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, str),
    "User-Agent": serialization.serialize_param(request.headers.UserAgent, str),
    "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, str),
    "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, str),
    "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, str),
    "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, str),
    "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
        body = serialization.serialize(request.body, type(None)),
      )

    @staticmethod
    def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request':
      return READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Request(
          userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       scheduleID = serialization.deserialize(request.path[5], int),       itemId = serialization.deserialize(request.path[7], int),
    CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), str),
    UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
    XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), str),
    XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), str),
    XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), str),
    XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), str),
    XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str)
    )

    @staticmethod
    def to_raw_response(serialization: Wirespec.Serializer, response: 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response') -> Wirespec.RawResponse:
      match response:
        case READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response200():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, ScheduleInstanceRead),
          )
        case READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response400():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody),
          )
        case _:
          raise Exception("Cannot match response with status: " + str(response.status))
    @staticmethod
    def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> 'READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response':
      match response.status_code:
        case 200:
          return READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response200(
            body = serialization.deserialize(response.body, ScheduleInstanceRead),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case 400:
          return READ_ScheduleInstance_for_User_MonetaryAccount_ScheduleEndpoint.Response400(
            body = serialization.deserialize(response.body, READ_ScheduleInstance_for_User_MonetaryAccount_Schedule400ResponseBody),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case _: 
          raise Exception("Cannot match response with status: " + str(response.status_code))



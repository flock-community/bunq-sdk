from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

from ..model.ShareInviteMonetaryAccountInquiry import ShareInviteMonetaryAccountInquiry
from ..model.ShareInviteMonetaryAccountInquiryUpdate import ShareInviteMonetaryAccountInquiryUpdate
from ..model.UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody import UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody

class UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[ShareInviteMonetaryAccountInquiry]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
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
    def body(self) -> ShareInviteMonetaryAccountInquiry:
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

    _body:  ShareInviteMonetaryAccountInquiry
    _headers: Headers
    _queries: Queries
    _path: Path
    method: Wirespec.Method = Wirespec.Method.PUT

    def __init__(self, userID: int, monetaryaccountID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: ShareInviteMonetaryAccountInquiry):
      self._path = UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, itemId = itemId)
      self._queries =UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request.Queries()
      self._headers = UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self._body = body

  @dataclass
  class Response200(Wirespec.Response[ShareInviteMonetaryAccountInquiryUpdate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> ShareInviteMonetaryAccountInquiryUpdate:
      return self._body

    _body: ShareInviteMonetaryAccountInquiryUpdate
    _headers: Headers
    status: int = 200

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: ShareInviteMonetaryAccountInquiryUpdate):
      self._headers = UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  @dataclass
  class Response400(Wirespec.Response[UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody:
      return self._body

    _body: UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody
    _headers: Headers
    status: int = 400

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody):
      self._headers = UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  Response = Response200 | Response400

  class Handler(Wirespec.Endpoint.Handler):
    @abstractmethod
    def UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount(self, req: 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request') -> 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response': pass

  class Convert(Wirespec.Endpoint.Convert[Request, Response]):
    @staticmethod
    def to_raw_request(serialization: Wirespec.Serializer, request: 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request') -> Wirespec.RawRequest:
      return Wirespec.RawRequest(
        path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetaryaccountID), "share-invite-monetary-account-inquiry", str(request.path.itemId)],
        method = request.method.value,
        queries = {},
        headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, str),
    "User-Agent": serialization.serialize_param(request.headers.UserAgent, str),
    "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, str),
    "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, str),
    "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, str),
    "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, str),
    "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
        body = serialization.serialize(request.body, ShareInviteMonetaryAccountInquiry),
      )

    @staticmethod
    def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request':
      return UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Request(
          userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       itemId = serialization.deserialize(request.path[5], int),
    CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), str),
    UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
    XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), str),
    XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), str),
    XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), str),
    XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), str),
    XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
          body = serialization.deserialize(request.body, ShareInviteMonetaryAccountInquiry),
    )

    @staticmethod
    def to_raw_response(serialization: Wirespec.Serializer, response: 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response') -> Wirespec.RawResponse:
      match response:
        case UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response200():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, ShareInviteMonetaryAccountInquiryUpdate),
          )
        case UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response400():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody),
          )
        case _:
          raise Exception("Cannot match response with status: " + str(response.status))
    @staticmethod
    def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> 'UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response':
      match response.status_code:
        case 200:
          return UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response200(
            body = serialization.deserialize(response.body, ShareInviteMonetaryAccountInquiryUpdate),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case 400:
          return UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount.Response400(
            body = serialization.deserialize(response.body, UPDATE_ShareInviteMonetaryAccountInquiry_for_User_MonetaryAccount400ResponseBody),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case _: 
          raise Exception("Cannot match response with status: " + str(response.status_code))



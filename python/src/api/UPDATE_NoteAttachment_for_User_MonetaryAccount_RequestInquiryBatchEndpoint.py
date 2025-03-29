from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

from .NoteAttachmentRequestInquiryBatch import NoteAttachmentRequestInquiryBatch
from .NoteAttachmentRequestInquiryBatchUpdate import NoteAttachmentRequestInquiryBatchUpdate
from .UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody import UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody

class UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentRequestInquiryBatch]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        requestinquirybatchID: int 
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
    def body(self) -> NoteAttachmentRequestInquiryBatch:
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

    _body:  NoteAttachmentRequestInquiryBatch
    _headers: Headers
    _queries: Queries
    _path: Path
    method: Wirespec.Method = Wirespec.Method.PUT

    def __init__(self, userID: int, monetaryaccountID: int, requestinquirybatchID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentRequestInquiryBatch):
      self._path = UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, requestinquirybatchID = requestinquirybatchID, itemId = itemId)
      self._queries = UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Queries()
      self._headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self._body = body

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentRequestInquiryBatchUpdate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> NoteAttachmentRequestInquiryBatchUpdate:
      return self._body

    _body: NoteAttachmentRequestInquiryBatchUpdate
    _headers: Headers
    status: int = 200

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentRequestInquiryBatchUpdate):
      self._headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  @dataclass
  class Response400(Wirespec.Response[UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody:
      return self._body

    _body: UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody
    _headers: Headers
    status: int = 400

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody):
      self._headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  Response = Response200 | Response400

  class Handler(Wirespec.Endpoint.Handler):
    @abstractmethod
    def UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch(self, req: 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request') -> 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response': pass

  class Convert(Wirespec.Endpoint.Convert[Request, Response]):
    @staticmethod
    def to_raw_request(serialization: Wirespec.Serializer, request: 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request') -> Wirespec.RawRequest:
      return Wirespec.RawRequest(
        path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetaryaccountID), "request-inquiry-batch", str(request.path.requestinquirybatchID), "note-attachment", str(request.path.itemId)],
        method = request.method.value,
        queries = {},
        headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, str),
    "User-Agent": serialization.serialize_param(request.headers.UserAgent, str),
    "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, str),
    "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, str),
    "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, str),
    "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, str),
    "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
        body = serialization.serialize(request.body, NoteAttachmentRequestInquiryBatch),
      )

    @staticmethod
    def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request':
      return UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request(
          userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       requestinquirybatchID = serialization.deserialize(request.path[5], int),       itemId = serialization.deserialize(request.path[7], int),
    CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), str),
    UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
    XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), str),
    XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), str),
    XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), str),
    XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), str),
    XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
          body = serialization.deserialize(request.body, NoteAttachmentRequestInquiryBatch),
    )

    @staticmethod
    def to_raw_response(serialization: Wirespec.Serializer, response: 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response') -> Wirespec.RawResponse:
      match response:
        case UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, NoteAttachmentRequestInquiryBatchUpdate),
          )
        case UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody),
          )
        case _:
          raise Exception("Cannot match response with status: " + str(response.status))
    @staticmethod
    def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> 'UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response':
      match response.status_code:
        case 200:
          return UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200(
            body = serialization.deserialize(response.body, NoteAttachmentRequestInquiryBatchUpdate),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case 400:
          return UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400(
            body = serialization.deserialize(response.body, UPDATE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case _: 
          raise Exception("Cannot match response with status: " + str(response.status_code))



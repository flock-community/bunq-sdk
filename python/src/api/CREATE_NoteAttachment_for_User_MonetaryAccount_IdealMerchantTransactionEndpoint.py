from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

from .NoteAttachmentIdealMerchantTransaction import NoteAttachmentIdealMerchantTransaction
from .NoteAttachmentIdealMerchantTransactionCreate import NoteAttachmentIdealMerchantTransactionCreate
from .CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody import CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody

class CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentIdealMerchantTransaction]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        idealmerchanttransactionID: int 
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
    def body(self) -> NoteAttachmentIdealMerchantTransaction:
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

    _body:  NoteAttachmentIdealMerchantTransaction
    _headers: Headers
    _queries: Queries
    _path: Path
    method: Wirespec.Method = Wirespec.Method.POST

    def __init__(self, userID: int, monetaryaccountID: int, idealmerchanttransactionID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentIdealMerchantTransaction):
      self._path = CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, idealmerchanttransactionID = idealmerchanttransactionID)
      self._queries = CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request.Queries()
      self._headers = CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self._body = body

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentIdealMerchantTransactionCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> NoteAttachmentIdealMerchantTransactionCreate:
      return self._body

    _body: NoteAttachmentIdealMerchantTransactionCreate
    _headers: Headers
    status: int = 200

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentIdealMerchantTransactionCreate):
      self._headers = CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: 'Optional[str]'
        XBunqClientRequestId: 'Optional[str]'
        XBunqServerSignature: 'Optional[str]'

    @property
    def headers(self) -> Headers:
      return self._headers

    @property
    def body(self) -> CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody:
      return self._body

    _body: CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody
    _headers: Headers
    status: int = 400

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody):
      self._headers = CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self._body = body

  Response = Response200 | Response400

  class Handler(Wirespec.Endpoint.Handler):
    @abstractmethod
    def CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction(self, req: 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request') -> 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response': pass

  class Convert(Wirespec.Endpoint.Convert[Request, Response]):
    @staticmethod
    def to_raw_request(serialization: Wirespec.Serializer, request: 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request') -> Wirespec.RawRequest:
      return Wirespec.RawRequest(
        path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetaryaccountID), "ideal-merchant-transaction", str(request.path.idealmerchanttransactionID), "note-attachment"],
        method = request.method.value,
        queries = {},
        headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, str),
    "User-Agent": serialization.serialize_param(request.headers.UserAgent, str),
    "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, str),
    "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, str),
    "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, str),
    "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, str),
    "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
        body = serialization.serialize(request.body, NoteAttachmentIdealMerchantTransaction),
      )

    @staticmethod
    def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request':
      return CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Request(
          userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       idealmerchanttransactionID = serialization.deserialize(request.path[5], int),
    CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), str),
    UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
    XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), str),
    XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), str),
    XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), str),
    XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), str),
    XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
          body = serialization.deserialize(request.body, NoteAttachmentIdealMerchantTransaction),
    )

    @staticmethod
    def to_raw_response(serialization: Wirespec.Serializer, response: 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response') -> Wirespec.RawResponse:
      match response:
        case CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response200():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, NoteAttachmentIdealMerchantTransactionCreate),
          )
        case CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response400():
          return Wirespec.RawResponse(
            status_code = response.status,
            headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, str), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, str), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, str)},
            body = serialization.serialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody),
          )
        case _:
          raise Exception("Cannot match response with status: " + str(response.status))
    @staticmethod
    def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> 'CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response':
      match response.status_code:
        case 200:
          return CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response200(
            body = serialization.deserialize(response.body, NoteAttachmentIdealMerchantTransactionCreate),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case 400:
          return CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransactionEndpoint.Response400(
            body = serialization.deserialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_IdealMerchantTransaction400ResponseBody),
            XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), str),
            XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), str),
            XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), str)
          )
        case _: 
          raise Exception("Cannot match response with status: " + str(response.status_code))



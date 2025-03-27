from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteAttachmentSofortMerchantTransaction import NoteAttachmentSofortMerchantTransaction
from .NoteAttachmentSofortMerchantTransactionCreate import NoteAttachmentSofortMerchantTransactionCreate
from .CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody import CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody

class CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentSofortMerchantTransaction]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        sofortmerchanttransactionID: int 
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
 
    body: NoteAttachmentSofortMerchantTransaction = None
    method: Wirespec.Method = Wirespec.Method.POST
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, sofortmerchanttransactionID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentSofortMerchantTransaction):
      self.path = CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, sofortmerchanttransactionID = sofortmerchanttransactionID)
      self.queries = CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Request.Queries()
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self.body = body

  @staticmethod
  def to_raw_request(serialization: Wirespec.Serializer, request: Request) -> Wirespec.RawRequest:
    return Wirespec.RawRequest(
      path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetary-accountID), "sofort-merchant-transaction", str(request.path.sofort-merchant-transactionID), "note-attachment"],
      method = request.method.value,
      queries = {},
      headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "User-Agent": serialization.serialize_param(request.headers.UserAgent, str), "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteAttachmentSofortMerchantTransaction),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       sofortmerchanttransactionID = serialization.deserialize(request.path[5], int),
  CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
  XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
        body = serialization.deserialize(request.body, NoteAttachmentSofortMerchantTransaction),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentSofortMerchantTransactionCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteAttachmentSofortMerchantTransactionCreate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentSofortMerchantTransactionCreate):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteAttachmentSofortMerchantTransactionCreate),
        )
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteAttachmentSofortMerchantTransactionCreate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case 400:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransactionEndpoint.Response400(
          body = serialization.deserialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def CREATE_NoteAttachment_for_User_MonetaryAccount_SofortMerchantTransaction(self, req: Request) -> Response: pass

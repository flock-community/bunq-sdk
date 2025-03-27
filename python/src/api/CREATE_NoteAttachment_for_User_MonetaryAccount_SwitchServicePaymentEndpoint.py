from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment import NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment
from .NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate import NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate
from .CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody import CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody

class CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        switchservicepaymentID: int 
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
 
    body: NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment = None
    method: Wirespec.Method = Wirespec.Method.POST
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, switchservicepaymentID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment):
      self.path = CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, switchservicepaymentID = switchservicepaymentID)
      self.queries = CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Request.Queries()
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetary-accountID), "switch-service-payment", str(request.path.switch-service-paymentID), "note-attachment"],
      method = request.method.value,
      queries = {},
      headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "User-Agent": serialization.serialize_param(request.headers.UserAgent, str), "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       switchservicepaymentID = serialization.deserialize(request.path[5], int),
  CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
  XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
        body = serialization.deserialize(request.body, NoteAttachmentBankSwitchServiceNetherlandsIncomingPayment),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate),
        )
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteAttachmentBankSwitchServiceNetherlandsIncomingPaymentCreate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case 400:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePaymentEndpoint.Response400(
          body = serialization.deserialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def CREATE_NoteAttachment_for_User_MonetaryAccount_SwitchServicePayment(self, req: Request) -> Response: pass

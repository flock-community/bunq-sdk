from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteAttachmentSchedulePayment import NoteAttachmentSchedulePayment
from .NoteAttachmentSchedulePaymentCreate import NoteAttachmentSchedulePaymentCreate
from .CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody import CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody

class CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentSchedulePayment]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        schedulepaymentID: int 
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
 
    body: NoteAttachmentSchedulePayment = None
    method: Wirespec.Method = Wirespec.Method.POST
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, schedulepaymentID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentSchedulePayment):
      self.path = CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, schedulepaymentID = schedulepaymentID)
      self.queries = CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Request.Queries()
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", request.path.userID, "monetary-account", request.path.monetary-accountID, "schedule-payment", request.path.schedule-paymentID, "note-attachment"],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteAttachmentSchedulePayment),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       schedulepaymentID = serialization.deserialize(request.path[5], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str),
        body = serialization.deserialize(request.body, NoteAttachmentSchedulePayment),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentSchedulePaymentCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteAttachmentSchedulePaymentCreate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentSchedulePaymentCreate):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody):
      self.headers = CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteAttachmentSchedulePaymentCreate),
        )
      case CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteAttachmentSchedulePaymentCreate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePaymentEndpoint.Response400(
          body = serialization.deserialize(response.body, CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def CREATE_NoteAttachment_for_User_MonetaryAccount_SchedulePayment(self, req: Request) -> Response: pass

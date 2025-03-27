from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteAttachmentScheduleRequest import NoteAttachmentScheduleRequest
from .NoteAttachmentScheduleRequestUpdate import NoteAttachmentScheduleRequestUpdate
from .UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody import UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody

class UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteAttachmentScheduleRequest]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        schedulerequestinquiryID: int 
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
 
    body: NoteAttachmentScheduleRequest = None
    method: Wirespec.Method = Wirespec.Method.PUT
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, schedulerequestinquiryID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteAttachmentScheduleRequest):
      self.path = UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, schedulerequestinquiryID = schedulerequestinquiryID, itemId = itemId)
      self.queries = UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Request.Queries()
      self.headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", str(request.path.userID), "monetary-account", str(request.path.monetary-accountID), "schedule-request-inquiry", str(request.path.schedule-request-inquiryID), "note-attachment", str(request.path.itemId)],
      method = request.method.value,
      queries = {},
      headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "User-Agent": serialization.serialize_param(request.headers.UserAgent, str), "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteAttachmentScheduleRequest),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       schedulerequestinquiryID = serialization.deserialize(request.path[5], int),       itemId = serialization.deserialize(request.path[7], int),
  CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
  XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str),
        body = serialization.deserialize(request.body, NoteAttachmentScheduleRequest),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentScheduleRequestUpdate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteAttachmentScheduleRequestUpdate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentScheduleRequestUpdate):
      self.headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody):
      self.headers = UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteAttachmentScheduleRequestUpdate),
        )
      case UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteAttachmentScheduleRequestUpdate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case 400:
        return UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiryEndpoint.Response400(
          body = serialization.deserialize(response.body, UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def UPDATE_NoteAttachment_for_User_MonetaryAccount_ScheduleRequestInquiry(self, req: Request) -> Response: pass

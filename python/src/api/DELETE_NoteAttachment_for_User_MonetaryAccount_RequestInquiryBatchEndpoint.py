from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteAttachmentRequestInquiryBatchDelete import NoteAttachmentRequestInquiryBatchDelete
from .DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody import DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody

class DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[None]):
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
        CacheControl: Optional[str]
        UserAgent: str
        XBunqLanguage: Optional[str]
        XBunqRegion: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqGeolocation: Optional[str]
        XBunqClientAuthentication: str
 
    body: None = None
    method: Wirespec.Method = Wirespec.Method.DELETE
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, requestinquirybatchID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str):
      self.path = DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, requestinquirybatchID = requestinquirybatchID, itemId = itemId)
      self.queries = DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Queries()
      self.headers = DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request.Headers(  CacheControl = CacheControl,
        UserAgent = UserAgent,
        XBunqLanguage = XBunqLanguage,
        XBunqRegion = XBunqRegion,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqGeolocation = XBunqGeolocation,
        XBunqClientAuthentication = XBunqClientAuthentication)
      self.body = None

  @staticmethod
  def to_raw_request(serialization: Wirespec.Serializer, request: Request) -> Wirespec.RawRequest:
    return Wirespec.RawRequest(
      path = ["user", request.path.userID, "monetary-account", request.path.monetary-accountID, "request-inquiry-batch", request.path.request-inquiry-batchID, "note-attachment", request.path.itemId],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, None),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       requestinquirybatchID = serialization.deserialize(request.path[5], int),       itemId = serialization.deserialize(request.path[7], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str)
  )

  @dataclass
  class Response200(Wirespec.Response[NoteAttachmentRequestInquiryBatchDelete]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteAttachmentRequestInquiryBatchDelete = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteAttachmentRequestInquiryBatchDelete):
      self.headers = DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody):
      self.headers = DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteAttachmentRequestInquiryBatchDelete),
        )
      case DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteAttachmentRequestInquiryBatchDelete),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatchEndpoint.Response400(
          body = serialization.deserialize(response.body, DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def DELETE_NoteAttachment_for_User_MonetaryAccount_RequestInquiryBatch(self, req: Request) -> Response: pass

from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseTransferRequirement import TransferwiseTransferRequirement
from .TransferwiseTransferRequirementCreate import TransferwiseTransferRequirementCreate
from .CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody import CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody

class CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[TransferwiseTransferRequirement]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        transferwisequoteID: int 
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
 
    body: TransferwiseTransferRequirement = None
    method: Wirespec.Method = Wirespec.Method.POST
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, transferwisequoteID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: TransferwiseTransferRequirement):
      self.path = CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Request.Path(userID = userID, transferwisequoteID = transferwisequoteID)
      self.queries = CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Request.Queries()
      self.headers = CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", request.path.userID, "transferwise-quote", request.path.transferwise-quoteID, "transferwise-transfer-requirement"],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, TransferwiseTransferRequirement),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       transferwisequoteID = serialization.deserialize(request.path[3], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str),
        body = serialization.deserialize(request.body, TransferwiseTransferRequirement),
  )

  @dataclass
  class Response200(Wirespec.Response[TransferwiseTransferRequirementCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: TransferwiseTransferRequirementCreate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: TransferwiseTransferRequirementCreate):
      self.headers = CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody):
      self.headers = CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, TransferwiseTransferRequirementCreate),
        )
      case CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response200(
          body = serialization.deserialize(response.body, TransferwiseTransferRequirementCreate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuoteEndpoint.Response400(
          body = serialization.deserialize(response.body, CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def CREATE_TransferwiseTransferRequirement_for_User_TransferwiseQuote(self, req: Request) -> Response: pass

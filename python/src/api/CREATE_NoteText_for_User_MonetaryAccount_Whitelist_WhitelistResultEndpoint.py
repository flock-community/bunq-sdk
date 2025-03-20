from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteTextWhitelistResult import NoteTextWhitelistResult
from .NoteTextWhitelistResultCreate import NoteTextWhitelistResultCreate
from .CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody import CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody

class CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteTextWhitelistResult]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        whitelistID: int 
        whitelistresultID: int 
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
 
    body: NoteTextWhitelistResult = None
    method: Wirespec.Method = Wirespec.Method.POST
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, whitelistID: int, whitelistresultID: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteTextWhitelistResult):
      self.path = CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, whitelistID = whitelistID, whitelistresultID = whitelistresultID)
      self.queries = CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Request.Queries()
      self.headers = CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", request.path.userID, "monetary-account", request.path.monetary-accountID, "whitelist", request.path.whitelistID, "whitelist-result", request.path.whitelist-resultID, "note-text"],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteTextWhitelistResult),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       whitelistID = serialization.deserialize(request.path[5], int),       whitelistresultID = serialization.deserialize(request.path[7], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str),
        body = serialization.deserialize(request.body, NoteTextWhitelistResult),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteTextWhitelistResultCreate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteTextWhitelistResultCreate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteTextWhitelistResultCreate):
      self.headers = CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody):
      self.headers = CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteTextWhitelistResultCreate),
        )
      case CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteTextWhitelistResultCreate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResultEndpoint.Response400(
          body = serialization.deserialize(response.body, CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def CREATE_NoteText_for_User_MonetaryAccount_Whitelist_WhitelistResult(self, req: Request) -> Response: pass

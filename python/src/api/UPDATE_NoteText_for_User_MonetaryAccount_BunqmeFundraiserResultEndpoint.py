from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .NoteTextBunqMeFundraiserResult import NoteTextBunqMeFundraiserResult
from .NoteTextBunqMeFundraiserResultUpdate import NoteTextBunqMeFundraiserResultUpdate
from .UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody import UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody

class UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[NoteTextBunqMeFundraiserResult]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
        bunqmefundraiserresultID: int 
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
 
    body: NoteTextBunqMeFundraiserResult = None
    method: Wirespec.Method = Wirespec.Method.PUT
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, bunqmefundraiserresultID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: NoteTextBunqMeFundraiserResult):
      self.path = UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, bunqmefundraiserresultID = bunqmefundraiserresultID, itemId = itemId)
      self.queries = UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Request.Queries()
      self.headers = UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", request.path.userID, "monetary-account", request.path.monetary-accountID, "bunqme-fundraiser-result", request.path.bunqme-fundraiser-resultID, "note-text", request.path.itemId],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, NoteTextBunqMeFundraiserResult),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       bunqmefundraiserresultID = serialization.deserialize(request.path[5], int),       itemId = serialization.deserialize(request.path[7], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str),
        body = serialization.deserialize(request.body, NoteTextBunqMeFundraiserResult),
  )

  @dataclass
  class Response200(Wirespec.Response[NoteTextBunqMeFundraiserResultUpdate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: NoteTextBunqMeFundraiserResultUpdate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: NoteTextBunqMeFundraiserResultUpdate):
      self.headers = UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody):
      self.headers = UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, NoteTextBunqMeFundraiserResultUpdate),
        )
      case UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response200(
          body = serialization.deserialize(response.body, NoteTextBunqMeFundraiserResultUpdate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResultEndpoint.Response400(
          body = serialization.deserialize(response.body, UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def UPDATE_NoteText_for_User_MonetaryAccount_BunqmeFundraiserResult(self, req: Request) -> Response: pass

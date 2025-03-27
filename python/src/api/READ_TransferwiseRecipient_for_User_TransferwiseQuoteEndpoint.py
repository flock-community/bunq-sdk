from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseAccountQuoteRead import TransferwiseAccountQuoteRead
from .READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody import READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody

class READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[None]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        transferwisequoteID: int 
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
    method: Wirespec.Method = Wirespec.Method.GET
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, transferwisequoteID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str):
      self.path = READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Request.Path(userID = userID, transferwisequoteID = transferwisequoteID, itemId = itemId)
      self.queries = READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Request.Queries()
      self.headers = READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", str(request.path.userID), "transferwise-quote", str(request.path.transferwise-quoteID), "transferwise-recipient", str(request.path.itemId)],
      method = request.method.value,
      queries = {},
      headers = {"Cache-Control": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "User-Agent": serialization.serialize_param(request.headers.UserAgent, str), "X-Bunq-Language": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "X-Bunq-Region": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Geolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "X-Bunq-Client-Authentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, None),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       transferwisequoteID = serialization.deserialize(request.path[3], int),       itemId = serialization.deserialize(request.path[5], int),
  CacheControl = serialization.deserialize_param(request.headers.get("Cache-Control".lower()), Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers.get("User-Agent".lower()), str),
  XBunqLanguage = serialization.deserialize_param(request.headers.get("X-Bunq-Language".lower()), Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers.get("X-Bunq-Region".lower()), Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers.get("X-Bunq-Geolocation".lower()), Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers.get("X-Bunq-Client-Authentication".lower()), str)
  )

  @dataclass
  class Response200(Wirespec.Response[TransferwiseAccountQuoteRead]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: TransferwiseAccountQuoteRead = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: TransferwiseAccountQuoteRead):
      self.headers = READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody):
      self.headers = READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, TransferwiseAccountQuoteRead),
        )
      case READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"X-Bunq-Client-Response-Id": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "X-Bunq-Client-Request-Id": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "X-Bunq-Server-Signature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response200(
          body = serialization.deserialize(response.body, TransferwiseAccountQuoteRead),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case 400:
        return READ_TransferwiseRecipient_for_User_TransferwiseQuoteEndpoint.Response400(
          body = serialization.deserialize(response.body, READ_TransferwiseRecipient_for_User_TransferwiseQuote400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Response-Id".lower()), Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers.get("X-Bunq-Client-Request-Id".lower()), Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers.get("X-Bunq-Server-Signature".lower()), Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def READ_TransferwiseRecipient_for_User_TransferwiseQuote(self, req: Request) -> Response: pass

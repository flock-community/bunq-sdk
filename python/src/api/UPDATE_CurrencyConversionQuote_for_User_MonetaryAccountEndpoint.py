from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .CurrencyConversionQuote import CurrencyConversionQuote
from .CurrencyConversionQuoteUpdate import CurrencyConversionQuoteUpdate
from .UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody import UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody

class UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint (Wirespec.Endpoint):
  @dataclass
  class Request(Wirespec.Request[CurrencyConversionQuote]):
    @dataclass
    class Path (Wirespec.Request.Path):
        userID: int 
        monetaryaccountID: int 
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
 
    body: CurrencyConversionQuote = None
    method: Wirespec.Method = Wirespec.Method.PUT
    path: Path = None
    queries: Queries = None
    headers: Headers = None

    def __init__(self, userID: int, monetaryaccountID: int, itemId: int, CacheControl: Optional[str], UserAgent: str, XBunqLanguage: Optional[str], XBunqRegion: Optional[str], XBunqClientRequestId: Optional[str], XBunqGeolocation: Optional[str], XBunqClientAuthentication: str, body: CurrencyConversionQuote):
      self.path = UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Request.Path(userID = userID, monetaryaccountID = monetaryaccountID, itemId = itemId)
      self.queries = UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Request.Queries()
      self.headers = UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Request.Headers(  CacheControl = CacheControl,
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
      path = ["user", request.path.userID, "monetary-account", request.path.monetary-accountID, "currency-conversion-quote", request.path.itemId],
      method = request.method.value,
      queries = {},
      headers = {"CacheControl": serialization.serialize_param(request.headers.CacheControl, Optional[str]), "UserAgent": serialization.serialize_param(request.headers.UserAgent, str), "XBunqLanguage": serialization.serialize_param(request.headers.XBunqLanguage, Optional[str]), "XBunqRegion": serialization.serialize_param(request.headers.XBunqRegion, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(request.headers.XBunqClientRequestId, Optional[str]), "XBunqGeolocation": serialization.serialize_param(request.headers.XBunqGeolocation, Optional[str]), "XBunqClientAuthentication": serialization.serialize_param(request.headers.XBunqClientAuthentication, str)},
      body = serialization.serialize(request.body, CurrencyConversionQuote),
    )

  @staticmethod
  def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
    return UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Request(
        userID = serialization.deserialize(request.path[1], int),       monetaryaccountID = serialization.deserialize(request.path[3], int),       itemId = serialization.deserialize(request.path[5], int),
  CacheControl = serialization.deserialize_param(request.headers["Cache-Control"], Optional[str]),
  UserAgent = serialization.deserialize_param(request.headers["User-Agent"], str),
  XBunqLanguage = serialization.deserialize_param(request.headers["X-Bunq-Language"], Optional[str]),
  XBunqRegion = serialization.deserialize_param(request.headers["X-Bunq-Region"], Optional[str]),
  XBunqClientRequestId = serialization.deserialize_param(request.headers["X-Bunq-Client-Request-Id"], Optional[str]),
  XBunqGeolocation = serialization.deserialize_param(request.headers["X-Bunq-Geolocation"], Optional[str]),
  XBunqClientAuthentication = serialization.deserialize_param(request.headers["X-Bunq-Client-Authentication"], str),
        body = serialization.deserialize(request.body, CurrencyConversionQuote),
  )

  @dataclass
  class Response200(Wirespec.Response[CurrencyConversionQuoteUpdate]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: CurrencyConversionQuoteUpdate = None
    status: int = 200
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: CurrencyConversionQuoteUpdate):
      self.headers = UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response200.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  @dataclass
  class Response400(Wirespec.Response[UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody]):
    @dataclass
    class Headers (Wirespec.Response.Headers):
        XBunqClientResponseId: Optional[str]
        XBunqClientRequestId: Optional[str]
        XBunqServerSignature: Optional[str]

    body: UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody = None
    status: int = 400
    headers: Headers = None

    def __init__(self, XBunqClientResponseId: Optional[str], XBunqClientRequestId: Optional[str], XBunqServerSignature: Optional[str], body: UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody):
      self.headers = UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response400.Headers(  XBunqClientResponseId = XBunqClientResponseId,
        XBunqClientRequestId = XBunqClientRequestId,
        XBunqServerSignature = XBunqServerSignature)
      self.body = body

  Response = Response200 | Response400

  @staticmethod
  def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
    match response:
      case UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response200():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, CurrencyConversionQuoteUpdate),
        )
      case UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response400():
        return Wirespec.RawResponse(
          status_code = response.status,
          headers = {"XBunqClientResponseId": serialization.serialize_param(response.headers.XBunqClientResponseId, Optional[str]), "XBunqClientRequestId": serialization.serialize_param(response.headers.XBunqClientRequestId, Optional[str]), "XBunqServerSignature": serialization.serialize_param(response.headers.XBunqServerSignature, Optional[str])},
          body = serialization.serialize(response.body, UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody),
        )

  @staticmethod
  def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
    match response.status_code:
      case 200:
        return UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response200(
          body = serialization.deserialize(response.body, CurrencyConversionQuoteUpdate),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case 400:
        return UPDATE_CurrencyConversionQuote_for_User_MonetaryAccountEndpoint.Response400(
          body = serialization.deserialize(response.body, UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount400ResponseBody),
          XBunqClientResponseId = serialization.deserialize_param(response.headers["X-Bunq-Client-Response-Id"], Optional[str]),
          XBunqClientRequestId = serialization.deserialize_param(response.headers["X-Bunq-Client-Request-Id"], Optional[str]),
          XBunqServerSignature = serialization.deserialize_param(response.headers["X-Bunq-Server-Signature"], Optional[str])
        )
      case _: 
        raise Exception("Cannot match response with status: " + str(response.status_code))

  @abstractmethod
  def UPDATE_CurrencyConversionQuote_for_User_MonetaryAccount(self, req: Request) -> Response: pass

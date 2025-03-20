from abc import abstractmethod
from dataclasses import dataclass
from shared import T, Wirespec

@dataclass
class PotentialTodoDto:
    name: str
    done: bool

@dataclass
class Token:
    iss: str

@dataclass
class TodoDto:
    id: str
    name: str
    done: bool

@dataclass
class Error:
    code: int
    description: str

class PutTodoEndpoint (Wirespec.Endpoint):
    @dataclass
    class Request(Wirespec.Request[PotentialTodoDto]):
        @dataclass
        class Path (Wirespec.Request.Path):
            id: str
        @dataclass
        class Queries (Wirespec.Request.Queries):
            done: bool
        @dataclass
        class Headers (Wirespec.Request.Headers):
            token: Token

        body: PotentialTodoDto = None
        method: Wirespec.Method = Wirespec.Method.PUT
        path: Path = None
        queries: Queries = None
        headers: Headers = None

        def __init__(self, id: str, done: bool, token: Token, body: PotentialTodoDto):
            self.path = PutTodoEndpoint.Request.Path(id = id)
            self.queries = PutTodoEndpoint.Request.Queries(done = done)
            self.headers = PutTodoEndpoint.Request.Headers(token = token)
            self.body = body

    @staticmethod
    def to_raw_request(serialization: Wirespec.Serializer, request: Request) -> Wirespec.RawRequest:
        return Wirespec.RawRequest(
            path = ["todos", request.path.id],
            method = request.method.value,
            queries = {"done": serialization.serialize_param(request.queries.done, bool)},
            headers = {"token": serialization.serialize_param(request.headers.token, Token)},
            body = serialization.serialize(request.body, PotentialTodoDto),
        )

    @staticmethod
    def from_raw_request(serialization: Wirespec.Deserializer, request: Wirespec.RawRequest) -> Request:
        return PutTodoEndpoint.Request(
            id = serialization.deserialize(request.path[1], str),
            done = serialization.deserialize_param(request.queries["done"], bool),
            token = serialization.deserialize_param(request.headers["token"], Token),
            body = serialization.deserialize(request.body, PotentialTodoDto),
        )

    @dataclass
    class Response200(Wirespec.Response[TodoDto]):
        @dataclass
        class Headers (Wirespec.Response.Headers): pass

        body: TodoDto = None
        status: int = 200
        headers: Headers = None

        def __init__(self, body: TodoDto):
            self.headers = PutTodoEndpoint.Response200.Headers()
            self.body = body

    @dataclass
    class Response201(Wirespec.Response[TodoDto]):
        @dataclass
        class Headers (Wirespec.Response.Headers):
            token: Token

        body: TodoDto = None
        status: int = 201
        headers: Headers = None

        def __init__(self, token: Token, body: TodoDto):
            self.headers = PutTodoEndpoint.Response201.Headers(token = token)
            self.body = body

    @dataclass
    class Response500(Wirespec.Response[Error]):
        @dataclass
        class Headers (Wirespec.Response.Headers): pass

        body: Error = None
        status: int = 500
        headers: Headers = None

        def __init__(self, body: Error):
            self.headers = PutTodoEndpoint.Response500.Headers()
            self.body = body

    Response = Response200 | Response201 | Response500

    @staticmethod
    def to_raw_response(serialization: Wirespec.Serializer, response: Response) -> Wirespec.RawResponse:
        match response:
            case PutTodoEndpoint.Response200():
                return Wirespec.RawResponse(
                    status_code = response.status,
                    headers = {},
                    body = serialization.serialize(response.body, TodoDto),
                )
            case PutTodoEndpoint.Response201():
                return Wirespec.RawResponse(
                    status_code = response.status,
                    headers = {"token": serialization.serialize_param(response.headers.token, Token)},
                    body = serialization.serialize(response.body, TodoDto),
                )
            case PutTodoEndpoint.Response500():
                return Wirespec.RawResponse(
                    status_code = response.status,
                    headers = {},
                    body = serialization.serialize(response.body, Error),
                )


    @staticmethod
    def from_raw_response(serialization: Wirespec.Deserializer, response: Wirespec.RawResponse) -> Response:
        match response.status_code:
            case 200:
                return PutTodoEndpoint.Response200(
                    body = serialization.deserialize(response.body, TodoDto),
                )
            case 201:
                return PutTodoEndpoint.Response201(
                    body = serialization.deserialize(response.body, TodoDto),
                    token = serialization.deserialize_param(response.headers["token"], Token)
                )
            case 500:
                return PutTodoEndpoint.Response500(
                    body = serialization.deserialize(response.body, Error),
                )
            case _:
                raise Exception("Cannot match response with status: " + str(response.status_code))

    @abstractmethod
    def PutTodo(self, req: Request) -> Response: pass

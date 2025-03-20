from openapi import Error, PutTodoEndpoint
from openapi import Token, PotentialTodoDto, TodoDto



error = Error(666, 'Hearts')

print(error)

queries = PutTodoEndpoint.Request.Queries(
    done = False
)

mockReq = PutTodoEndpoint.Request(
    id = '123',
    done = False,
    token = Token(
        iss='abc'
    ),
    body=PotentialTodoDto(
        name = 'test',
        done=False
    )
)


mockRes = PutTodoEndpoint.Response200(
    body=TodoDto(
        id='123',
        name='test',
        done=False
    )
)

class Client(PutTodoEndpoint):
    def PutTodo(self, req: PutTodoEndpoint.Request) -> PutTodoEndpoint.Response:
        serde = Serialization()

        print("xxx")
        raw_req = PutTodoEndpoint.to_raw_request(serde, req)
        print(raw_req)
        x = PutTodoEndpoint.from_raw_request(serde, raw_req)
        print(x)

        print("yyy")
        print(mockRes)
        raw_res = PutTodoEndpoint.to_raw_response(serde, mockRes)
        print(raw_res)
        y = PutTodoEndpoint.from_raw_response(serde, raw_res)
        print(y)

        return mockRes

print("---")
print(mockReq)
print(mockReq.path)
print(mockReq.body)

print("---")
print(mockRes.headers)
print(mockRes.body)

def run():
    client = Client()
    t = client.PutTodo(mockReq)
    print(t.body)
    match client.PutTodo(mockReq):
        case PutTodoEndpoint.Response200(body):
            return body.name
        case PutTodoEndpoint.Response201(body):
            return body.name
        case PutTodoEndpoint.Response500(body):
            return body.code

print("+++")
print(run())
from signing import Signing
from context import Context
from transport import Serialization, send

from api.wirespec import Wirespec

def handler(signing: Signing, context: Context):
    serialization = Serialization()
    token = context.session_token



    def handle(endpoint:Wirespec.Endpoint, req: Wirespec.Request) -> Wirespec.Response:

        if token is None:
            raise Exception("Token is None")

        raw_req: Wirespec.RawRequest = endpoint.Convert.to_raw_request(serialization, req)
        raw_req.headers["X-Bunq-Client-Authentication"] = [token]
        raw_res = send(signing, raw_req)

        return endpoint.Convert.from_raw_response(serialization, raw_res)

    return handle
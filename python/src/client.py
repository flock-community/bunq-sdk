from api import (
    CREATE_InstallationEndpoint,
    CREATE_DeviceServerEndpoint,
    CREATE_SessionServerEndpoint,
    READ_UserEndpoint)
from api.shared.Wirespec import Wirespec
from signing import sign_data, generate_rsa_key_pair
import requests

baseUrl = "https://public-api.sandbox.bunq.com/v1/"
private_key_pem, public_key_pem = generate_rsa_key_pair()

def handler(serialization: Wirespec.Serialization, endpoint:type, req: Wirespec.Request) -> Wirespec.Response:
    raw_req: Wirespec.RawRequest = endpoint.to_raw_request(serialization, req)
    headers = dict(map(lambda kv: (kv[0], kv[1][0]), raw_req.headers.items()))
    
    if headers.get("X-Bunq-Client-Authentication") == "":
        del headers["X-Bunq-Client-Authentication"]

    if headers.get("X-Bunq-Geolocation") is None:
        del headers["X-Bunq-Geolocation"]

    if headers.get("X-Bunq-Region") is None:
        del headers["X-Bunq-Region"]

    signature_header = {'X-Bunq-Client-Signature':  sign_data(raw_req.body, private_key_pem)} if raw_req.body is not None else{}

    res  = requests.request(
        method = raw_req.method,
        url = baseUrl + '/'.join(raw_req.path),
        headers = {**headers, **signature_header},
        data = raw_req.body)
    headers = dict(map(lambda kv: (kv[0].lower(), [kv[1]]), res.headers.items()))
    raw_res = Wirespec.RawResponse(res.status_code, headers, res.text)
    try:
        return endpoint.from_raw_response(serialization, raw_res)
    except Exception as e:
        print(res.text)

class Client(
    CREATE_InstallationEndpoint,
    CREATE_DeviceServerEndpoint,
    CREATE_SessionServerEndpoint,
    READ_UserEndpoint):

    def __init__(self, serialization: Wirespec.Serialization):
        self.serialization = serialization

    def CREATE_Installation(self, req):
        return handler(self.serialization, CREATE_InstallationEndpoint, req)

    def CREATE_DeviceServer(self, req):
        return handler(self.serialization, CREATE_DeviceServerEndpoint, req)

    def CREATE_SessionServer(self, req):
        return handler(self.serialization, CREATE_SessionServerEndpoint, req)

    def READ_User(self, req):
        return handler(self.serialization, READ_UserEndpoint, req)



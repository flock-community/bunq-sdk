from typing import Dict, List, TypeVar, Type

from src.api import (CREATE_InstallationEndpoint,
                     CREATE_DeviceServerEndpoint,
                     CREATE_SessionServerEndpoint,
                     List_all_MonetaryAccountBank_for_UserEndpoint,
                     READ_UserEndpoint)

from src.api.shared.Wirespec import Wirespec

from src.signing import sign_data, generate_rsa_key_pair

import requests

Endpoint = TypeVar('Endpoint', bound=Type[Wirespec.Endpoint])
REQ = TypeVar('REQ', bound=Wirespec.Request)

baseUrl = "https://public-api.sandbox.bunq.com/v1/"
private_key_pem, public_key_pem = generate_rsa_key_pair()

def handler(serialization: Wirespec.Serialization, endpoint:Endpoint, req: Wirespec.Request) -> Wirespec.Response:
    raw_req: Wirespec.RawRequest = endpoint.Convert.to_raw_request(serialization, req)
    req_headers = dict(map(lambda kv: (kv[0], next(iter(kv[1]), None)), raw_req.headers.items()))

    if req_headers.get("X-Bunq-Client-Authentication") == "":
        del req_headers["X-Bunq-Client-Authentication"]

    if req_headers.get("X-Bunq-Geolocation") is None:
        del req_headers["X-Bunq-Geolocation"]

    if req_headers.get("X-Bunq-Region") is None:
        del req_headers["X-Bunq-Region"]

    signature_header = {'X-Bunq-Client-Signature':  sign_data(raw_req.body, private_key_pem)} if raw_req.body is not None else{}

    res  = requests.request(
        method = raw_req.method,
        url = baseUrl + '/'.join(raw_req.path),
        headers = {**req_headers, **signature_header},
        data = raw_req.body)
    res_headers:Dict[str, List[str]] = dict(map(lambda kv: (kv[0].lower(), list(kv[1])), res.headers.items()))
    raw_res = Wirespec.RawResponse(res.status_code, res_headers, res.text)

    return endpoint.Convert.from_raw_response(serialization, raw_res)

class Client(
    CREATE_InstallationEndpoint.Handler,
    CREATE_DeviceServerEndpoint.Handler,
    CREATE_SessionServerEndpoint.Handler,
    List_all_MonetaryAccountBank_for_UserEndpoint.Handler,
    READ_UserEndpoint.Handler
):

    def __init__(self, serialization: Wirespec.Serialization):
        self.serialization = serialization

    def CREATE_Installation(self, req):
        return handler(self.serialization, CREATE_InstallationEndpoint, req)

    def CREATE_DeviceServer(self, req):
        return handler(self.serialization, CREATE_DeviceServerEndpoint, req)

    def CREATE_SessionServer(self, req):
        return handler(self.serialization, CREATE_SessionServerEndpoint, req)

    def List_all_MonetaryAccountBank_for_User(self, req):
        return handler(self.serialization, List_all_MonetaryAccountBank_for_UserEndpoint, req)

    def READ_User(self, req):
        return handler(self.serialization, READ_UserEndpoint, req)



import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import List, TypeVar, Dict, Type, get_origin, get_args
from functools import reduce
from dacite import from_dict
import requests

from api.wirespec import Wirespec, T

from signing import sign_data, generate_rsa_key_pair

baseUrl = "https://public-api.sandbox.bunq.com/v1/"

private_key_pem, public_key_pem = generate_rsa_key_pair()


class Serialization(Wirespec.Serialization):

    def serialize(self, value: T, t: Type[T]) -> str:
        if value is None:
            return ""
        else:
            if is_dataclass(value) and not isinstance(value, type):
                dataclass_dict = asdict(value)
                return json.dumps(dataclass_dict)
            else:
                raise Exception('Unsupported type')


    def deserialize(self, value: str | None, t: Type[T]):
        if t == str or t == int or t == bool:
            return value
        else:
            if value is None:
                return None

            data = json.loads(value)

            if "Response" in data:
                res_data = data.get("Response")
                origin = get_origin(t)
                if origin is list:
                    generic = get_args(t)[0]
                    return list(map(lambda it: from_dict(data_class=generic, data=next(iter(it.values()))), res_data))
                else:
                    def add(acc: dict, cur: dict): return {**acc, **cur}
                    return from_dict(data_class=t, data=reduce(add, res_data, {}))
            else:
                raise Exception("Invalid response")

    def serialize_param(self, value: T, t: type) -> List[str]:
        if value is None:
            return []
        else:
            return [str(value)]

    def deserialize_param(self, value:list[str] | None, t: Type[T]):
        if value is None:
            return []
        else:
            return value

def handler(serialization: Wirespec.Serialization, endpoint:Wirespec.Endpoint, req: Wirespec.Request) -> Wirespec.Response:
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

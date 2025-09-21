import json
from dataclasses import asdict, is_dataclass
from functools import reduce
from typing import List, Dict, Type, get_origin, get_args

import requests
from dacite import from_dict

from api.wirespec import Wirespec, T
from signing import Signing


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
                    def add(acc: dict, cur: dict):
                        return {**acc, **cur}

                    return from_dict(data_class=t, data=reduce(add, res_data, {}))
            else:
                raise Exception("Invalid response")

    def serialize_param(self, value: T, t: type) -> List[str]:
        if value is None:
            return []
        else:
            return [str(value)]

    def deserialize_param(self, value: list[str] | None, t: Type[T]):
        if value is None:
            return []
        else:
            return value


def send(config, raw_req: Wirespec.RawRequest) -> Wirespec.RawResponse:
    req_headers = dict(map(lambda kv: (kv[0], next(iter(kv[1]), None)), raw_req.headers.items()))

    signed_data = Signing.sign_data(config, raw_req.body)
    signature_header = {'X-Bunq-Client-Signature': signed_data}
    res = requests.request(
        method=raw_req.method,
        url=config.bunq_server.base_url + '/'.join(raw_req.path),
        headers={**req_headers, **signature_header},
        data=raw_req.body)

    res_headers: Dict[str, List[str]] = dict(map(lambda kv: (kv[0].lower(), list(kv[1])), res.headers.items()))

    return Wirespec.RawResponse(res.status_code, res_headers, res.text)

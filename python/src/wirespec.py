import json, dataclasses
from typing import List
from functools import reduce
from dacite import from_dict

from shared import Wirespec, T

class Serialization(Wirespec.Serialization):

    def serialize(self, value: T, t: type) -> str:
        if t is None:
            return None
        else:
            return json.dumps(dataclasses.asdict(value))

    def serialize_param(self, value: T, t: type) -> List[str]:
        if value is None:
            return [value]
        else:
            return [str(value)]

    def deserialize_param(self, value:list[str], t: type) -> List[str]:
        return ["TEST"]

    def deserialize(self, value:str, t: type):
        if t == str or t == int or t == bool:
            return value
        else:
            data = json.loads(value)
            def add(acc: dict, cur: dict):
                return {**acc, **cur}

            if "Response" in data:
                j = reduce(add, data.get("Response"), {})
                return from_dict(data_class=t, data=j)
            else:
                raise Exception("Invalid response")
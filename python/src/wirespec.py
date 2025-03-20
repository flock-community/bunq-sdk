import json, dataclasses
from typing import List

from shared import Wirespec, T

class Serialization(Wirespec.Serialization):

    def serialize(self, value: T, t: type) -> str:
        return json.dumps(dataclasses.asdict(value))

    def serialize_param(self, value: T, t: type) -> List[str]:
        return ["TEST"]

    def deserialize_param(self, value:list[str], t: type) -> List[str]:
        return ["TEST"]

    def deserialize(self, value:str, t: type):
        print(t)
        if t == str or t == int or t == bool:
            return value
        else:
            j = json.loads(value)
            return t(**j)
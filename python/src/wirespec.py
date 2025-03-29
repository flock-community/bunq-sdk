import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import List, TypeVar, Dict
from functools import reduce
from dacite import from_dict

from src.api.shared.Wirespec import Wirespec, T

class Serialization(Wirespec.Serialization):

    def serialize(self, value: T, t: type[T]) -> str:
        if value is None:
            return ""
        else:
            if is_dataclass(value) and not isinstance(value, type):
                dataclass_dict = asdict(value)
                return json.dumps(dataclass_dict)
            else:
                raise Exception('Unsupported type')


    def deserialize(self, value: str | None, t: type[T]):
        if t == str or t == int or t == bool:
            return value
        else:
            if value is None:
                return None

            data = json.loads(value)
            def add(acc: dict, cur: dict):
                return {**acc, **cur}

            if "Response" in data:
                data = reduce(add, data.get("Response"), {})
                return from_dict(data_class=t, data=data)
            else:
                raise Exception("Invalid response")

    def serialize_param(self, value: T, t: type) -> List[str]:
        if value is None:
            return []
        else:
            return [str(value)]

    def deserialize_param(self, value:list[str] | None, t: type[T]):
        if value is None:
            return []
        else:
            return value

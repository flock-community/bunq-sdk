import json
from dataclasses import asdict, dataclass, is_dataclass
from typing import List, TypeVar, Dict, Type, get_origin, get_args
from functools import reduce
from dacite import from_dict

from .api.wirespec import Wirespec, T

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

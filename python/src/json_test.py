from dataclasses import dataclass
import json

json_data_str = """
{
   "PK" : "Foo",
   "SK" : "Bar",
   "eventtype" : "blah",
   "result" : "something",
   "type" : "badger",
   "status" : "active"
}
"""

@dataclass
class Dejlog:
    PK: str
    SK: str
    eventtype: str
    result: str
    type: str
    status: str

def serdes[T](json_srt: str, o:type):
    json_obj = json.loads(json_srt)
    return o(**json_obj)



x = serdes(json_data_str, Dejlog)
print(x)
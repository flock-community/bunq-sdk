from typing import Dict, List, TypeVar, Type

from api.endpoint.CREATE_Installation import CREATE_Installation
from api.endpoint.CREATE_DeviceServer import CREATE_DeviceServer
from api.endpoint.CREATE_SessionServer import CREATE_SessionServer
from api.endpoint.List_all_MonetaryAccountBank_for_User import List_all_MonetaryAccountBank_for_User
from api.endpoint.READ_User import READ_User

from api.wirespec import Wirespec

from signing import generate_rsa_key_pair
from wirespec import handler

Endpoint = TypeVar('Endpoint', bound=Type[Wirespec.Endpoint])
REQ = TypeVar('REQ', bound=Wirespec.Request)


class Client(
    CREATE_Installation.Handler,
    CREATE_DeviceServer.Handler,
    CREATE_SessionServer.Handler,
    List_all_MonetaryAccountBank_for_User.Handler,
    READ_User.Handler
):

    def __init__(self, serialization: Wirespec.Serialization):
        self.serialization = serialization

    def CREATE_Installation(self, req):
        return handler(self.serialization, CREATE_Installation, req)

    def CREATE_DeviceServer(self, req):
        return handler(self.serialization, CREATE_DeviceServer, req)

    def CREATE_SessionServer(self, req):
        return handler(self.serialization, CREATE_SessionServer, req)

    def List_all_MonetaryAccountBank_for_User(self, req):
        return handler(self.serialization, List_all_MonetaryAccountBank_for_User, req)

    def READ_User(self, req):
        return handler(self.serialization, READ_User, req)

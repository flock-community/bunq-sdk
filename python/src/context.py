from .api.endpoint.CREATE_Installation import CREATE_Installation
from .api.endpoint.CREATE_DeviceServer import CREATE_DeviceServer
from .api.endpoint.CREATE_SessionServer import CREATE_SessionServer

from .api.model.DeviceServer import DeviceServer
from .api.model.Installation import Installation
from .api.model.SessionServer import SessionServer

from .client import Client
from .signing import generate_rsa_key_pair

from .wirespec import Serialization

class Context:
    serialization = Serialization()
    client = Client(serialization)

    private_key_pem, public_key_pem = generate_rsa_key_pair()



    def __init__(self, api_key: str, service_name: str):
        self.api_key = api_key
        self.service_name = service_name
        installation = self.create_installation(service_name)
        self.server_public_key = installation.ServerPublicKey.server_public_key
        device_server = self.create_device_server(service_name, api_key, installation.Token.token)
        self.device_id = device_server.Id.id
        session_server = self.create_session_server(service_name, api_key, installation.Token.token)
        self.session_id = session_server.Id.id
        self.session_token = session_server.Token.token
        self.user_id = session_server.UserPerson.id

    def create_installation(self, service_name:str) -> Installation:
        body = Installation(
            client_public_key = self.public_key_pem
        )
        req = CREATE_Installation.Request(
            CacheControl = None,
            UserAgent = service_name,
            XBunqLanguage = None,
            XBunqRegion = None,
            XBunqClientRequestId = None,
            XBunqGeolocation = None,
            XBunqClientAuthentication = "",
            body = body
        )
        res = self.client.CREATE_Installation(req)
        match res:
            case CREATE_Installation.Response200(body=installation):
                return installation
            case _:
                raise Exception("Cannot create installation")

    def create_device_server(self, service_name:str, api_key:str, token:str) -> DeviceServer:
        body = DeviceServer(
            description = service_name,
            secret = api_key,
            permitted_ips = ["*"]
        )
        req = CREATE_DeviceServer.Request(
            CacheControl = None,
            UserAgent = service_name,
            XBunqLanguage = None,
            XBunqRegion = None,
            XBunqClientRequestId = None,
            XBunqGeolocation = None,
            XBunqClientAuthentication = token,
            body = body
        )
        match self.client.CREATE_DeviceServer(req):
            case CREATE_DeviceServer.Response200(body=device_server):
                return device_server
            case _:
                raise Exception("Cannot create device server")

    def create_session_server(self, service_name:str, api_key:str, token:str) -> SessionServer:
        body = SessionServer(
            secret = api_key,
        )
        req = CREATE_SessionServer.Request(
            CacheControl = None,
            UserAgent = service_name,
            XBunqLanguage = None,
            XBunqRegion = None,
            XBunqClientRequestId = None,
            XBunqGeolocation = None,
            XBunqClientAuthentication = token,
            body = body
        )
        match self.client.CREATE_SessionServer(req):
            case CREATE_SessionServer.Response200(body=server_session):
                return server_session
            case _:
                raise Exception("Cannot create device server")

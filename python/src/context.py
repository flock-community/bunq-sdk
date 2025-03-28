from dataclasses import dataclass

from api.CREATE_InstallationEndpoint import CREATE_InstallationEndpoint
from api.CREATE_DeviceServerEndpoint import CREATE_DeviceServerEndpoint
from api.CREATE_SessionServerEndpoint import CREATE_SessionServerEndpoint

from api.DeviceServer import DeviceServer
from api.Installation import Installation
from api.SessionServer import SessionServer
from client import Client
from signing import generate_rsa_key_pair

from wirespec import Serialization

@dataclass
class Context:

    api_key: str
    service_name: str

    server_public_key: str
    device_id: int
    session_id: int
    session_token: str
    user_id: int

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

    def create_installation(self, service_name:str):
        body = Installation(
            client_public_key = self.public_key_pem
        )
        req = CREATE_InstallationEndpoint.Request(
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
            case CREATE_InstallationEndpoint.Response200(body=installation):
                return installation
            case _:
                raise Exception("Cannot create installation")

    def create_device_server(self, service_name:str, api_key:str, token:str):
        body = DeviceServer(
            description = service_name,
            secret = api_key,
            permitted_ips = ["*"]
        )
        req = CREATE_DeviceServerEndpoint.Request(
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
            case CREATE_DeviceServerEndpoint.Response200(body=device_server):
                return device_server
            case _:
                raise Exception("Cannot create device server")

    def create_session_server(self, service_name:str, api_key:str, token:str):
        body = SessionServer(
            secret = api_key,
        )
        req = CREATE_SessionServerEndpoint.Request(
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
            case CREATE_SessionServerEndpoint.Response200(body=server_session):
                return server_session
            case _:
                raise Exception("Cannot create device server")

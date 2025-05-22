from api.endpoint import CREATE_Installation, CREATE_DeviceServer, CREATE_SessionServer
from api.model import InstallationCreate, DeviceServerCreate, SessionServerCreate

from api.model.DeviceServer import DeviceServer
from api.model.Installation import Installation
from api.model.SessionServer import SessionServer

from api.sdk import Sdk
from signing import generate_rsa_key_pair

from wirespec import Serialization, handler

class Context:
    serialization = Serialization()
    client = Sdk(handler, serialization)

    private_key_pem, public_key_pem = generate_rsa_key_pair()

    def __init__(self, api_key: str, service_name: str):
        self.api_key = api_key
        self.service_name = service_name
        installation = self.create_installation(service_name)
        if installation.ServerPublicKey is None:
            raise Exception("Installation does not have server public key")
        if installation.Token is None or installation.Token.token is None:
            raise Exception("Installation does not have token")
        self.server_public_key = installation.ServerPublicKey.server_public_key
        device_server = self.create_device_server(service_name, api_key, installation.Token.token)
        if device_server.Id is None:
            raise Exception("Device server does not have id")
        self.device_id = device_server.Id.id
        session_server = self.create_session_server(service_name, api_key, installation.Token.token)
        if session_server.Id is None:
            raise Exception("Session server does not have id")
        self.session_id = session_server.Id.id
        if session_server.Token is None:
            raise Exception("Session server does not have token")
        self.session_token = session_server.Token.token
        if session_server.UserPerson is None:
            raise Exception("Session server does not have user person")
        self.user_id = session_server.UserPerson.id

    def create_installation(self, service_name:str) -> InstallationCreate:
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
        print(type(res))
        match res:
            case CREATE_Installation.Response200(body=installation):
                return installation
            case e :
                print(e)
                raise Exception("Cannot create installation")

    def create_device_server(self, service_name:str, api_key:str, token:str) -> DeviceServerCreate:
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

    def create_session_server(self, service_name:str, api_key:str, token:str) -> SessionServerCreate:
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

from api.endpoint import CREATE_Installation, CREATE_DeviceServer, CREATE_SessionServer
from api.model import InstallationCreate, DeviceServerCreate, SessionServerCreate

from api.model.DeviceServer import DeviceServer
from api.model.Installation import Installation
from api.model.SessionServer import SessionServer

from signing import Signing
from config import Config
from transport import send, Serialization

class Context:

    def __init__(self, config: Config):
        self.config = config
        self.signing = Signing(config)
        self.private_key_pem, self.public_key_pem = self.signing.generate_rsa_key_pair()
        self.serialization = Serialization()

        self.api_key = config.api_key
        self.service_name = config.service_name
        installation = self.create_installation()
        if installation.ServerPublicKey is None:
            raise Exception("Installation does not have server public key")
        if installation.Token is None or installation.Token.token is None:
            raise Exception("Installation does not have token")
        self.server_public_key = installation.ServerPublicKey.server_public_key
        device_server = self.create_device_server(self.config.service_name, self.config.api_key, installation.Token.token)
        if device_server.id is None:
            raise Exception("Device server does not have id")
        self.device_id = device_server.id
        session_server = self.create_session_server(self.config.service_name, self.config.api_key, installation.Token.token)
        if session_server.Id is None:
            raise Exception("Session server does not have id")
        self.session_id = session_server.Id.id
        if session_server.Token is None:
            raise Exception("Session server does not have token")
        self.session_token = session_server.Token.token
        if session_server.UserPerson is None:
            raise Exception("Session server does not have user person")
        self.user_id = session_server.UserPerson.id

    def create_installation(self) -> InstallationCreate:
        body = Installation(
            client_public_key = self.public_key_pem
        )
        req = CREATE_Installation.Request(
            body = body
        )

        raw_req = CREATE_Installation.Convert.to_raw_request(self.serialization, req)
        raw_res = send(self.signing, raw_req)
        res = CREATE_Installation.Convert.from_raw_response(self.serialization, raw_res)

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
            body = body
        )

        raw_req = CREATE_DeviceServer.Convert.to_raw_request(self.serialization, req)
        raw_req.headers["X-Bunq-Client-Authentication"] = [token]
        raw_res = send(self.signing, raw_req)
        res = CREATE_DeviceServer.Convert.from_raw_response(self.serialization, raw_res)

        match res:
            case CREATE_DeviceServer.Response200(body=device_server):
                return device_server
            case _:
                raise Exception("Cannot create device server")

    def create_session_server(self, service_name:str, api_key:str, token:str) -> SessionServerCreate:
        body = SessionServer(
            secret = api_key,
        )
        req = CREATE_SessionServer.Request(
            body = body
        )

        raw_req = CREATE_SessionServer.Convert.to_raw_request(self.serialization, req)
        raw_req.headers["X-Bunq-Client-Authentication"] = [token]
        raw_res = send(self.signing, raw_req)
        res = CREATE_SessionServer.Convert.from_raw_response(self.serialization, raw_res)

        match res:
            case CREATE_SessionServer.Response200(body=server_session):
                return server_session
            case _:
                raise Exception("Cannot create session server")

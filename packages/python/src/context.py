from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from api.Client import Client
from api.endpoint.CreateInstallation import Response200 as InstallationResponse200
from api.endpoint.CreateDeviceServer import Response200 as DeviceServerResponse200
from api.endpoint.CreateSessionServer import Response200 as SessionServerResponse200
from api.model.InstallationCreate import InstallationCreate
from api.model.DeviceServerCreate import DeviceServerCreate
from api.model.SessionServerCreate import SessionServerCreate
from api.wirespec import Wirespec

from api.model.DeviceServer import DeviceServer
from api.model.Installation import Installation
from api.model.SessionServer import SessionServer

from config import Config
from transport import send, Serialization


@dataclass
class Context:
    """Context containing authentication and session information for bunq API requests"""
    server_public_key: str
    device_id: int
    session_id: int
    session_token: str
    user_id: int
    session_expiry_time: datetime
    installation_token: str
    config: Config


async def init_context(config: Config) -> Context:
    """Initialize a new context with fresh authentication.

    Async; sync callers can use `asyncio.run(init_context(config))`.
    """
    installation = await _create_installation(config)
    if installation.ServerPublicKey is None:
        raise Exception("No server public key")
    if installation.Token is None or installation.Token.token is None:
        raise Exception("Token not available")
    
    device_server = await _create_device_server(config, installation.Token.token)
    if device_server.Id is None:
        raise Exception("No device id")
    
    session_server = await _create_session_server(config, installation.Token.token)
    if session_server.Id is None:
        raise Exception("No session id")
    if session_server.Token is None:
        raise Exception("No session token")
    
    user_id = _get_user_id(session_server)
    session_timeout_seconds = _get_session_timeout(session_server)
    session_expiry_time = datetime.now() + timedelta(seconds=session_timeout_seconds)
    
    if installation.ServerPublicKey is None or installation.ServerPublicKey.server_public_key is None:
        raise Exception("Server public key not available")
    if device_server.Id is None or device_server.Id.id is None:
        raise Exception("Device ID not available")
    if session_server.Id is None or session_server.Id.id is None:
        raise Exception("Session ID not available")
    if session_server.Token is None or session_server.Token.token is None:
        raise Exception("Session token not available")
    if installation.Token is None or installation.Token.token is None:
        raise Exception("Installation token not available")
    
    return Context(
        server_public_key=installation.ServerPublicKey.server_public_key,
        device_id=device_server.Id.id,
        session_id=session_server.Id.id,
        session_token=session_server.Token.token,
        user_id=user_id,
        session_expiry_time=session_expiry_time,
        installation_token=installation.Token.token,
        config=config
    )

async def refresh_session(context: Context) -> Context:
    """
    Refresh this context's session.
    This recreates the session with the same device and installation but gets a new session token.
    
    Args:
        context: The existing context to refresh
        
    Returns:
        A new Context with refreshed session information
    """
    session_server = await _create_session_server(context.config, context.installation_token)
    if session_server.Id is None:
        raise Exception("No session id")
    if session_server.Token is None:
        raise Exception("No session token")
    
    user_id = _get_user_id(session_server)
    session_timeout_seconds = _get_session_timeout(session_server)
    session_expiry_time = datetime.now() + timedelta(seconds=session_timeout_seconds)
    
    if session_server.Id is None or session_server.Id.id is None:
        raise Exception("Session ID not available")
    if session_server.Token is None or session_server.Token.token is None:
        raise Exception("Session token not available")
    
    return Context(
        server_public_key=context.server_public_key,
        device_id=context.device_id,
        session_id=session_server.Id.id,
        session_token=session_server.Token.token,
        user_id=user_id,
        session_expiry_time=session_expiry_time,
        installation_token=context.installation_token,
        config=context.config
    )


class _SetupTransportation(Wirespec.Transportation):
    """Sends the unauthenticated or installation-token requests used to build a context."""

    def __init__(self, config: Config, token: Optional[str] = None):
        self.config = config
        self.token = token

    async def transport(self, request: Wirespec.RawRequest) -> Wirespec.RawResponse:
        if self.token is not None:
            request.headers["X-Bunq-Client-Authentication"] = [self.token]
        return await send(self.config, request)


def _setup_client(config: Config, token: Optional[str] = None) -> Client:
    return Client(Serialization(), _SetupTransportation(config, token))


async def _create_installation(config: Config) -> InstallationCreate:
    """Create installation with the bunq API"""
    res = await _setup_client(config).create_installation(
        Installation(client_public_key=config.signing_keys.public_key_as_pem()))

    match res:
        case InstallationResponse200(body=installation):
            return installation
        case _:
            raise Exception("Installation failed")


async def _create_device_server(config: Config, token: str) -> DeviceServerCreate:
    """Create device server with the bunq API"""
    res = await _setup_client(config, token).create_device_server(
        DeviceServer(description=config.service_name, secret=config.api_key, permitted_ips=["*"]))

    match res:
        case DeviceServerResponse200(body=device_server):
            return device_server
        case _:
            raise Exception("Device server creation failed")


async def _create_session_server(config: Config, token: str) -> SessionServerCreate:
    """Create session server with the bunq API"""
    res = await _setup_client(config, token).create_session_server(SessionServer(secret=config.api_key))

    match res:
        case SessionServerResponse200(body=server_session):
            return server_session
        case _:
            raise Exception("Session server creation failed")


def _get_user_id(session_server: SessionServerCreate) -> int:
    """Sessions can be for various types of users, of which only one is filled."""
    if session_server.UserPerson is not None and session_server.UserPerson.id is not None:
        return session_server.UserPerson.id
    elif session_server.UserCompany is not None and session_server.UserCompany.id is not None:
        return session_server.UserCompany.id
    elif session_server.UserApiKey is not None and session_server.UserApiKey.id is not None:
        return session_server.UserApiKey.id
    elif session_server.UserPaymentServiceProvider is not None and session_server.UserPaymentServiceProvider.id is not None:
        return session_server.UserPaymentServiceProvider.id
    else:
        raise Exception("No user id found in the SessionServerCreate response")


def _get_session_timeout(session_server: SessionServerCreate) -> int:
    """Extract session timeout from the user in the SessionServerCreate response."""
    timeout = None
    
    if session_server.UserPerson is not None:
        timeout = session_server.UserPerson.session_timeout
    elif session_server.UserCompany is not None:
        timeout = session_server.UserCompany.session_timeout
    elif session_server.UserPaymentServiceProvider is not None:
        timeout = session_server.UserPaymentServiceProvider.session_timeout
    elif session_server.UserApiKey is not None:
        timeout = _get_user_api_key_session_timeout(session_server.UserApiKey)
    
    if timeout is None:
        print("bunq - No session timeout found in session server response, using default of 30 minutes")
        return 30 * 60  # 30 minutes default
    
    return timeout


def _get_user_api_key_session_timeout(user_api_key) -> Optional[int]:
    """Extract session timeout for UserApiKey"""
    if user_api_key is None:
        return None
    
    if hasattr(user_api_key, 'granted_by_user') and user_api_key.granted_by_user is not None:
        return _get_user_api_key_anchored_user_session_timeout(user_api_key.granted_by_user)
    elif hasattr(user_api_key, 'requested_by_user') and user_api_key.requested_by_user is not None:
        return _get_user_api_key_anchored_user_session_timeout(user_api_key.requested_by_user)
    
    return None


def _get_user_api_key_anchored_user_session_timeout(anchored_user) -> Optional[int]:
    """Extract session timeout from UserApiKeyAnchoredUser"""
    if anchored_user is None:
        return None
    
    if hasattr(anchored_user, 'UserPerson') and anchored_user.UserPerson is not None:
        return anchored_user.UserPerson.session_timeout
    elif hasattr(anchored_user, 'UserCompany') and anchored_user.UserCompany is not None:
        return anchored_user.UserCompany.session_timeout
    elif hasattr(anchored_user, 'UserPaymentServiceProvider') and anchored_user.UserPaymentServiceProvider is not None:
        return anchored_user.UserPaymentServiceProvider.session_timeout
    
    return None

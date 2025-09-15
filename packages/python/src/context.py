from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from api.endpoint import CREATE_Installation, CREATE_DeviceServer, CREATE_SessionServer
from api.model import InstallationCreate, DeviceServerCreate, SessionServerCreate

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


def init_context(config: Config) -> Context:
    """Initialize a new context with fresh authentication"""
    serialization = Serialization()
    
    installation = _create_installation(config, serialization)
    if installation.ServerPublicKey is None:
        raise Exception("No server public key")
    if installation.Token is None or installation.Token.token is None:
        raise Exception("Token not available")
    
    device_server = _create_device_server(config, installation.Token.token, serialization)
    if device_server.Id is None:
        raise Exception("No device id")
    
    session_server = _create_session_server(config, installation.Token.token, serialization)
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

def refresh_session(context: Context) -> Context:
    """
    Refresh this context's session.
    This recreates the session with the same device and installation but gets a new session token.
    
    Args:
        context: The existing context to refresh
        
    Returns:
        A new Context with refreshed session information
    """
    serialization = Serialization()
    
    session_server = _create_session_server(context.config, context.installation_token, serialization)
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


def _create_installation(config: Config, serialization: Serialization) -> InstallationCreate:
    """Create installation with the bunq API"""
    body = Installation(
        client_public_key=config.signing_keys.public_key_as_pem()
    )
    req = CREATE_Installation.Request(body=body)

    raw_req = CREATE_Installation.Convert.to_raw_request(serialization, req)
    raw_res = send(config, raw_req)
    res = CREATE_Installation.Convert.from_raw_response(serialization, raw_res)

    match res:
        case CREATE_Installation.Response200(body=installation):
            return installation
        case _:
            raise Exception("Installation failed")


def _create_device_server(config: Config, token: str, serialization: Serialization) -> DeviceServerCreate:
    """Create device server with the bunq API"""
    body = DeviceServer(
        description=config.service_name,
        secret=config.api_key,
        permitted_ips=["*"]
    )
    req = CREATE_DeviceServer.Request(body=body)

    raw_req = CREATE_DeviceServer.Convert.to_raw_request(serialization, req)
    raw_req.headers["X-Bunq-Client-Authentication"] = [token]
    raw_res = send(config, raw_req)
    res = CREATE_DeviceServer.Convert.from_raw_response(serialization, raw_res)

    match res:
        case CREATE_DeviceServer.Response200(body=device_server):
            return device_server
        case _:
            raise Exception("Device server creation failed")


def _create_session_server(config: Config, token: str, serialization: Serialization) -> SessionServerCreate:
    """Create session server with the bunq API"""
    body = SessionServer(secret=config.api_key)
    req = CREATE_SessionServer.Request(body=body)

    raw_req = CREATE_SessionServer.Convert.to_raw_request(serialization, req)
    raw_req.headers["X-Bunq-Client-Authentication"] = [token]
    raw_res = send(config, raw_req)
    res = CREATE_SessionServer.Convert.from_raw_response(serialization, raw_res)

    match res:
        case CREATE_SessionServer.Response200(body=server_session):
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

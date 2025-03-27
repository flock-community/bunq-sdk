from bunq_lib import BunqClient
from api import READ_UserEndpoint
from client import Client
from src.context import Context

from src.signing import generate_rsa_key_pair
from wirespec import Serialization

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"

bunq_client = BunqClient(USER_API_KEY, service_name='PeterScript')

service_name='PeterScript'

serialization = Serialization()
api = Client(serialization)

context = Context(USER_API_KEY, service_name)


req = READ_UserEndpoint.Request(
    itemId = context.user_id,
    CacheControl = None,
    UserAgent = context.server_name,
    XBunqLanguage = None,
    XBunqRegion = None,
    XBunqClientRequestId = None,
    XBunqGeolocation = None,
    XBunqClientAuthentication = context.session_token,
)

res = api.READ_User(req)

match res:
    case READ_UserEndpoint.Response200(body):
        print(body.UserPerson.display_name)

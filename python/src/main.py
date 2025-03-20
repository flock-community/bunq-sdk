from bunq_lib import BunqClient
from api import READ_UserEndpoint
from wirespec import Serialization

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"

bunq_client = BunqClient(USER_API_KEY, service_name='PeterScript')


bunq_client.create_installation()
bunq_client.create_device_server()
bunq_client.create_session()


req = READ_UserEndpoint.Request(
    itemId = 1,
    CacheControl = None,
    UserAgent = "None",
    XBunqLanguage = None,
    XBunqRegion = None,
    XBunqClientRequestId = None,
    XBunqGeolocation = None,
    XBunqClientAuthentication = "None",
)

raw_request = READ_UserEndpoint.to_raw_request(Serialization(), req)

print(raw_request)
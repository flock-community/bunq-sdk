import unittest

from api.endpoint import READ_User, List_all_MonetaryAccountBank_for_User

from context import Context
from wirespec import Serialization, handler
from api.sdk import Sdk

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name='PeterScript'

serialization = Serialization()
sdk = Sdk(handler, serialization)
context = Context(USER_API_KEY, service_name)

class Testing(unittest.TestCase):

    def test_read_user_endpoint_test(self):
        req = READ_User.Request(
            itemId = context.user_id,
            CacheControl = None,
            UserAgent = context.service_name,
            XBunqLanguage = None,
            XBunqRegion = None,
            XBunqClientRequestId = None,
            XBunqGeolocation = None,
            XBunqClientAuthentication = context.session_token,
        )

        res = sdk.READ_User(req)

        match res:
            case READ_User.Response200(body):
                if body.UserPerson is None: raise Exception("User not found")
                self.assertEqual(body.UserPerson.display_name, "D. Byrne")

    def test_list_all_monetary_account_bank_for_User(self):

        req = List_all_MonetaryAccountBank_for_User.Request(
            userID = context.user_id,
            CacheControl = None,
            UserAgent = context.service_name,
            XBunqLanguage = None,
            XBunqRegion = None,
            XBunqClientRequestId = None,
            XBunqGeolocation = None,
            XBunqClientAuthentication = context.session_token,
        )

        res = sdk.List_all_MonetaryAccountBank_for_User(req)

        match res:
            case List_all_MonetaryAccountBank_for_User.Response200(body):
                self.assertEqual(body[0].display_name, "D. Byrne")

def main():
    unittest.main()

if __name__ == "__main__":
    main()

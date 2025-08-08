import unittest

from api.endpoint import READ_User, List_all_MonetaryAccountBank_for_User
from api.sdk import Sdk
from context import Context
from config import Config
from signing import Signing
from wirespec import Serialization, handler

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name = 'PeterScript'

serialization = Serialization()
config = Config(
    api_key = USER_API_KEY,
    service_name = service_name,
    public_key_file="../../../test/public_key.pem",
    private_key_file="../../../test/private_key.pem"
)
signing = Signing(config)
context = Context(config)
sdk = Sdk(handler(signing, context), serialization)


class Testing(unittest.TestCase):

    def test_read_user_endpoint_test(self):

        res = sdk.READ_User(
            itemId=context.user_id,
        )

        match res:
            case READ_User.Response200(body):
                if body.UserPerson is None: raise Exception("User not found")
                self.assertEqual(body.UserPerson.display_name, "D. Byrne")

    def test_list_all_monetary_account_bank_for_User(self):

        res = sdk.List_all_MonetaryAccountBank_for_User(
            userID=context.user_id,
            count= None,
            newer_id= None,
            older_id= None,
        )

        match res:
            case List_all_MonetaryAccountBank_for_User.Response200(body):
                self.assertEqual(body[0].display_name, "D. Byrne")


def main():
    unittest.main()


if __name__ == "__main__":
    main()

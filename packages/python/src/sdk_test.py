import unittest

from api.endpoint import READ_User, List_all_MonetaryAccountBank_for_User
from api.sdk import Sdk
from config import Config
from context import init_context
from signing_keys import SigningKeysFromPem
from signing_test import PRIVATE_KEY_PEM, PUBLIC_KEY_PEM
from bunq_server import BUNQ_SANDBOX_SERVER
from wirespec import Serialization, handler

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name = 'PeterScript'

serialization = Serialization()
config = Config(
    bunq_server=BUNQ_SANDBOX_SERVER,
    api_key = USER_API_KEY,
    service_name = service_name,
    signing_keys = SigningKeysFromPem(PRIVATE_KEY_PEM, PUBLIC_KEY_PEM),
)

context = init_context(config)
sdk = Sdk(handler(context), serialization)


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

import unittest

from api.endpoint.ListAllMonetaryAccountBankForUser import Response200 as ListAccountsResponse200
from api.endpoint.ReadUser import Response200 as ReadUserResponse200
from bunq_server import BUNQ_SANDBOX_SERVER
from config import Config
from context import init_context
from signing_keys import SigningKeysFromPem
from signing_test import PRIVATE_KEY_PEM, PUBLIC_KEY_PEM
from wirespec import bunq_client

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"

config = Config(
    bunq_server=BUNQ_SANDBOX_SERVER,
    api_key=USER_API_KEY,
    service_name='PeterScript',
    signing_keys=SigningKeysFromPem(PRIVATE_KEY_PEM, PUBLIC_KEY_PEM),
)


class Testing(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.context = await init_context(config)
        self.client = bunq_client(self.context)

    async def test_read_user_endpoint_test(self):
        res = await self.client.read_user(itemId=self.context.user_id)

        match res:
            case ReadUserResponse200(body=body):
                if body.UserPerson is None: raise Exception("User not found")
                self.assertEqual(body.UserPerson.display_name, "D. Byrne")
            case _:
                self.fail(res)

    async def test_list_all_monetary_account_bank_for_user(self):
        res = await self.client.list_all_monetary_account_bank_for_user(
            userID=self.context.user_id,
            count=None,
            newer_id=None,
            older_id=None,
        )

        match res:
            case ListAccountsResponse200(body=body):
                self.assertEqual(body[0].display_name, "D. Byrne")
            case _:
                self.fail(res)


if __name__ == "__main__":
    unittest.main()

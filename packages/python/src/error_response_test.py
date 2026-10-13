import unittest

from api.endpoint.ReadUser import Response400, Response403, ReadUser
from api.wirespec import Wirespec
from transport import Serialization


class ErrorResponseTest(unittest.TestCase):

    def read_user(self, status: int, body: str):
        return ReadUser.fromRawResponse(Serialization(), Wirespec.RawResponse(status, {}, body.encode('utf-8')))

    def test_400_error_body_without_response_envelope_is_deserialized(self):
        response = self.read_user(400, '{"Error":[{"error_description":"Missing required field \\"currency\\"."}]}')

        self.assertIsInstance(response, Response400)
        self.assertEqual('Missing required field "currency".', response.body.Error[0].error_description)

    def test_status_other_than_200_and_400_is_a_typed_response(self):
        response = self.read_user(403, '{"Error":[{"error_description":"Insufficient authentication."}]}')

        self.assertIsInstance(response, Response403)
        self.assertEqual('Insufficient authentication.', response.body.Error[0].error_description)


if __name__ == '__main__':
    unittest.main()

import unittest

from src.client import Client
from src.context import Context
from src.signing import generate_rsa_key_pair, sign_data
from src.wirespec import Serialization

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name='PeterScript'

serialization = Serialization()
api = Client(serialization)

context = Context(USER_API_KEY, service_name)

class Testing(unittest.TestCase):

    def test_signing(self):
        print("Testing signing")
        private_key_pem, public_key_pem = generate_rsa_key_pair()
        res = sign_data("Hello", private_key_pem)
        print(res)
        self.assertEqual(res, "T/jCqiFSe1nj9keIq2Cdg5MISs69IIJa1BcmsQ+0iLTuKWNrbOcSS7lvEF7HSWiW8i7Vu4ofhTaw+iob75UB9qVpy8gZBd6UMSWKNUMDXtqj0LbUcov191m6eYLEme9hkg4R/5L9eEaTGvMuuEjxJ05/GgJe2wj2hhun1WoKGBaNCV9y7UrT6CXODMl45AprtttCpB5smjaCtfnW6NaIijHRanKjjIKLu7XaxYVuEFEYvsgm+aQKdKa1gi90qT48zt/R8MNLqoOH1P4NHAXXnplTh5j1BJEDKk1QMsZBS71KhbQU3y3dRjjf/+NqnCX6nZP35S2FZGg+mGiNv/Lirg==")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
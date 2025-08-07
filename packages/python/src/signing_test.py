import unittest

from signing import Signing
from config import Config

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name = 'PeterScript'

config = Config(
    api_key = USER_API_KEY,
    service_name = service_name,
    public_key_file="../../../test/public_key.pem",
    private_key_file="../../../test/private_key.pem"
)

signing = Signing(config)

class Testing(unittest.TestCase):

    def test_signing(self):
        print("Testing signing")
        res = signing.sign_data("Hello")
        print(res)
        self.assertEqual(res, "fR0Gyn8VfC8eCwq10x5eYAcxXh4nv6331hWAAr77l72zfFScbw3hFSE6iBNklCYc0mfnKezsuRo3re+fTNNHO1oZhfhjc9i4UYxTxBiOEslHrKx9NkXkBZh2RALx/LnhlpyMwB5BBOlFlNeR9Hyj5E8c/a2pObBZRmrZ3cgAnoWF8hhY5Y9XwLS2WIodYIPSQXuQMXyi1UBxhxAbniZ5m1uRSt8gaPmQGMCQtUzvZ8KUXtSvugGPsXHwh94EccZCfjS0sdIQK8AcZ8t5YL6bqkqJ7eVzbxoX6U1nOZVy3MxQMKQ/PFS297er6qsVsGwKbNfaTUvymEb46mM/gQdQDQ==")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
import unittest

from signing import Signing
from src.config import Config

USER_API_KEY = "sandbox_83f4f88a10706750ec2fdcbc1ce97b582a986f2846d33dcaaa974d95"
service_name = 'PeterScript'

config = Config(
    api_key = USER_API_KEY,
    service_name = service_name,
    public_key_file="../../public_key.pem",
    private_key_file="../../private_key.pem"
)

signing = Signing(config)

class Testing(unittest.TestCase):

    def test_signing(self):
        print("Testing signing")
        res = signing.sign_data("Hello")
        print(res)
        self.assertEqual(res, "yQlbXl0Odd96X2HG1/GdznujqEugb435bAsWv0jl+9fcEzdCSbXaqpeAVSK/PPzGL/Jxpl5ev1ehZVNB57Rvqwwp2zAGwvRVq4SxLd0D4ya3y9//Rs3ZvA0lW64ICqPENBTAEo1u0pQEoqopTZRee1puZBII57nR+pDGMHAHoJqPEhYFXmEB7a5Ba1lqVCOC7Sfb2zFxCMN6SUf1YTi6cxDqCPJ6NArzLrwRSdi0x4E1lUaD+1/OL913vdAGRERrq4GXzEhj50xiQpajY0OsjPiUErVkpfmntoSRf2GD+AHCBowqQwK6nYMiw7uBTCqL0bcYwo4i7m8WDdw1L6gV7w==")
def main():
    unittest.main()

if __name__ == "__main__":
    main()
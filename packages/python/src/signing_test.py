import unittest

from signing import generate_rsa_key_pair, sign_data

class Testing(unittest.TestCase):

    def test_signing(self):
        print("Testing signing")
        private_key_pem, public_key_pem = generate_rsa_key_pair()
        res = sign_data("Hello", private_key_pem)
        print(res)
        self.assertEqual(res, "yQlbXl0Odd96X2HG1/GdznujqEugb435bAsWv0jl+9fcEzdCSbXaqpeAVSK/PPzGL/Jxpl5ev1ehZVNB57Rvqwwp2zAGwvRVq4SxLd0D4ya3y9//Rs3ZvA0lW64ICqPENBTAEo1u0pQEoqopTZRee1puZBII57nR+pDGMHAHoJqPEhYFXmEB7a5Ba1lqVCOC7Sfb2zFxCMN6SUf1YTi6cxDqCPJ6NArzLrwRSdi0x4E1lUaD+1/OL913vdAGRERrq4GXzEhj50xiQpajY0OsjPiUErVkpfmntoSRf2GD+AHCBowqQwK6nYMiw7uBTCqL0bcYwo4i7m8WDdw1L6gV7w==")
def main():
    unittest.main()

if __name__ == "__main__":
    main()
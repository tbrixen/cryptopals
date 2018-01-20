import unittest
from blockcrypto import pkcs7_pad

class cryptopals_blockcrypto(unittest.TestCase):

    def test_pkcs7_of_single_block(self):
        block_size = 4
        data = bytes.fromhex("0011")
        expected = bytes.fromhex("00110202")
        result = pkcs7_pad(data, block_size)
        self.assertEqual(result.hex(), expected.hex())

    def test_pkcs7_of_multiple_blocks(self):
        block_size = 3
        data = bytes.fromhex("0011223344")
        expected = bytes.fromhex("001122334401")
        result = pkcs7_pad(data, block_size)
        self.assertEqual(result.hex(), expected.hex())

    def test_pkcs7_pad_of_full_block(self):
        block_size = 4
        data = bytes.fromhex("00112233")
        expected = bytes.fromhex("0011223304040404")
        result = pkcs7_pad(data, block_size)
        self.assertEqual(result.hex(), expected.hex())

    def test_pkcs7_pad_of_full_multiple_block(self):
        block_size = 4
        data = bytes.fromhex("0011223344556677")
        expected = bytes.fromhex("001122334455667704040404")
        result = pkcs7_pad(data, block_size)
        self.assertEqual(result.hex(), expected.hex())

if __name__ == '__main__':
    unittest.main()

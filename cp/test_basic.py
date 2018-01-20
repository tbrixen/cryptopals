import unittest
from basic import xor, expand_key, expand_key_and_xor, guess_key_for_single_byte_xor, hamming_distance, decrypt_aes_ecb

class cryptopals_basic(unittest.TestCase):

    def test_fixed_xor(self):
        a = bytes.fromhex('1c0111001f010100061a024b53535009181c')
        b = bytes.fromhex('686974207468652062756c6c277320657965')
        res = bytes.fromhex('746865206b696420646f6e277420706c6179')
        self.assertEqual(xor(a, b), res)

    def test_xor_equal_length(self):
        with self.assertRaisesRegex(BaseException, 'unequal length'):
            xor(bytes.fromhex("AA"), bytes.fromhex("BBAA"))

    def test_expand_key_of_single_byte(self):
        result = expand_key(bytes([9]), 3)
        self.assertEqual(result, bytes.fromhex("090909"))

    def test_expand_key_of_multiple_bytes(self):
        result = expand_key(bytes.fromhex("AABB"), 3)
        self.assertEqual(result, bytes.fromhex("AABBAA"))

    def test_expand_key_and_xor(self):
        result = expand_key_and_xor(bytes.fromhex("0102"), bytes([3]))
        self.assertEqual(result, bytes.fromhex("0201"))

    def test_expand_key_and_xor_challenge05(self):
        plaintext = ("Burning 'em, if you ain't quick and nimble\n"
                      "I go crazy when I hear a cymbal"
                    ).encode()
        key = b"ICE"
        expected = bytes.fromhex("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")
        actual = expand_key_and_xor(plaintext, key)
        self.assertEqual(actual, expected)

    def test_guess_key_for_single_byte_xor(self):
        text = b'Hello this is some english text'
        result = guess_key_for_single_byte_xor(text)
        self.assertEqual(result, bytes([0]))

    def test_guess_key_for_single_byte_xor_shifted(self):
        text = b'Hello this is some english text'
        ciphertext = expand_key_and_xor(text, bytes.fromhex("10"))
        result = guess_key_for_single_byte_xor(ciphertext)
        self.assertEqual(result, bytes([16]))

    def test_hamming_distance(self):
        a = b"this is a test"
        b = b"wokka wokka!!!"
        result = hamming_distance(a, b)
        self.assertIs(result, 37)

    def test_decrypt_aes_ecb_key_not_corrent_length(self):
        key = bytes.fromhex("01020304")
        data = bytes.fromhex("01020304")
        with self.assertRaisesRegex(ValueError, 'Key is not 16 bytes'):
            decrypt_aes_ecb(key, data)

    def test_decrypt_aes_ecb_data_not_corrent_length(self):
        key = bytes.fromhex("01020304010203040102030401020304")
        data = bytes.fromhex("01020304")
        with self.assertRaisesRegex(ValueError, 'Data is not a multiple of 16 bytes'):
            decrypt_aes_ecb(key, data)

    def test_decrypt_aes_ecb_(self):
        key =  b"YELLOW SUBMARINE"
        data = bytes.fromhex("091230aade3eb330dbaa4358f88d2a6c37b72d0cf4c22c344aec4142d00ce530")
        result = decrypt_aes_ecb(key, data)
        self.assertEqual(result, b"I'm back and I'm ringin' the bel")

if __name__ == '__main__':
    unittest.main()

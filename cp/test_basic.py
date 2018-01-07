import unittest
from basic import xor#, expandKey, expandKeyAndXor, countCharsIgnoreCase, guessKeyForSingleByteXor, hammingDistance, canReadNextByte, canReadNextBytes, readEveryXByte, decrypt_aes_ecb

class cryptopals_basic(unittest.TestCase):

    def test_fixed_xor(self):
        a = bytes.fromhex('1c0111001f010100061a024b53535009181c')
        b = bytes.fromhex('686974207468652062756c6c277320657965')
        res = bytes.fromhex('746865206b696420646f6e277420706c6179')
        self.assertEquals(xor(a, b), res)

    def test_xor_equal_length(self):
        with self.assertRaisesRegex(BaseException, 'unequal length'):
            xor(bytes.fromhex("AA"), bytes.fromhex("BBAA"))

    #def test_expand_key_of_single_bit(self):
    #    result = expandKey(Bits('0b1'), 4)
    #    self.assertEquals(result, Bits('0b1111'))

    #def test_expand_key_of_multiple_bits(self):
    #    result = expandKey(Bits('0b110'), 5)
    #    self.assertEquals(result, Bits('0b11011'))

    #def test_expand_key_and_xor(self):
    #    result = expandKeyAndXor(Bits('0b11001100'), Bits('0b110'))
    #    self.assertEquals(result, Bits('0b00010111'))
    #    self.assertIs(result.pos, 0)

#    def test_count_chars_ignore_case_in_string_upper_case(self):
#        haystack = Bits(bytes="anadsgGfAbf")
#        result = countCharsIgnoreCase(haystack, 'A');
#        self.assertIs(result, 3)
#
#    def test_count_chars_ignore_case_in_string_lower_case(self):
#        haystack = Bits(bytes="anadsgGfAbf")
#        result = countCharsIgnoreCase(haystack, 'a');
#        self.assertIs(result, 3)
#
#    def test_count_chars_ignore_case_in_string_no_match(self):
#        haystack = Bits(bytes="aaaa")
#        result = countCharsIgnoreCase(haystack, 'w');
#        self.assertIs(result, 0)
#
#    def test_count_chars_ignore_case_in_string_without_printable_char(self):
#        haystack = Bits(hex="0x0010181f")
#        result = countCharsIgnoreCase(haystack, 'a');
#        self.assertIs(result, 0)
#
#    def test_count_chars_ignore_case_in_string_mixed_printable_char(self):
#        haystack = Bits(hex="0x00611018411f")
#        result = countCharsIgnoreCase(haystack, 'a');
#        self.assertIs(result, 2)
#
#    def test_guess_key_for_single_byte_xor(self):
#        text = Bits(bytes='Hello this is some english text')
#        result = guessKeyForSingleByteXor(text)
#        self.assertIs(result.int, 0)
#
#    def test_guess_key_for_single_byte_xor_shifted(self):
#        text = Bits(bytes='Hello this is some english text')
#        result = guessKeyForSingleByteXor(expandKeyAndXor(text, Bits(hex="10")))
#        self.assertIs(result.int, 16)
#
#    def test_hamming_distance(self):
#        a = BitStream(bytes="this is a test")
#        b = BitStream(bytes="wokka wokka!!!")
#        result = hammingDistance(a, b)
#        self.assertIs(result, 37)
#
#    def test_can_read_next_byte(self):
#        data = BitStream(hex='00')
#        self.assertTrue(canReadNextByte(data))
#
#    def test_can_read_next_byte_one_off(self):
#        data = BitStream(hex='00')
#        data.pos = 1
#        self.assertFalse(canReadNextByte(data))
#
#    def test_can_read_next_byte_on_empty_stream(self):
#        data = BitStream()
#        self.assertFalse(canReadNextByte(data))
#
#    def test_can_read_next_zero_bytes(self):
#        data = BitStream()
#        self.assertTrue(canReadNextBytes(data, 0))
#
#    def test_can_read_next_single_byte(self):
#        data = BitStream(hex='41')
#        self.assertTrue(canReadNextBytes(data, 1))
#
#    def test_can_read_next_single_byte_fails(self):
#        data = BitStream()
#        self.assertFalse(canReadNextBytes(data, 1))
#
#    def test_can_read_next_multiple_byte_fails(self):
#        data = BitStream(hex='41')
#        self.assertFalse(canReadNextBytes(data, 2))
#
#    def test_can_read_next_multiple_byte(self):
#        data = BitStream(hex='4142')
#        self.assertTrue(canReadNextBytes(data, 2))
#
#    def test_can_read_next_multiple_byte_off_by_one(self):
#        data = BitStream(hex='4142')
#        data.pos = 1
#        self.assertFalse(canReadNextBytes(data, 2))
#
#    def test_read_every_x_bytes_of_empty_source(self):
#        data = BitStream()
#        result = readEveryXByte(data, 1)
#        self.assertIs(result.len, 0)
#
#    def test_read_every_1_bytes(self):
#        data = BitStream(hex="010203")
#        result = readEveryXByte(data, 1)
#        self.assertEquals(result, BitStream(hex="010203"))
#
#    def test_read_every_2_bytes(self):
#        data = BitStream(hex="010203")
#        result = readEveryXByte(data, 2)
#        self.assertEquals(result, BitStream(hex="0103"))
#
#    def test_decrypt_aes_ecb_key_not_corrent_length(self):
#        key = BitStream(hex="01020304")
#        data = BitStream(hex="01020304")
#        with self.assertRaisesRegexp(ValueError, 'Key is not 128 bits'):
#            decrypt_aes_ecb(key, data)
#
#    def test_decrypt_aes_ecb_data_not_corrent_length(self):
#        key = BitStream(hex="01020304010203040102030401020304")
#        data = BitStream(hex="01020304")
#        with self.assertRaisesRegexp(ValueError, 'Data is not a multiple of 16 bytes'):
#            decrypt_aes_ecb(key, data)
#
#    def test_decrypt_aes_ecb_(self):
#        key = BitStream(bytes="YELLOW SUBMARINE")
#        data = BitStream(hex="091230aade3eb330dbaa4358f88d2a6c37b72d0cf4c22c344aec4142d00ce530")
#        result = decrypt_aes_ecb(key, data)
#        self.assertEquals(result.bytes, BitStream(bytes="I'm back and I'm ringin' the bel").bytes)
#



if __name__ == '__main__':
    unittest.main()

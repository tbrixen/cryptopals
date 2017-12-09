import unittest
from basic import xor, expandKey, expandKeyAndXor, countCharsIgnoreCase, guessKeyForSingleByteXor
from bitstring import Bits, BitStream

class TestUM(unittest.TestCase):

    def test_simple(self):
        result = xor(Bits('0b111'), Bits('0b101'))
        self.assertEquals(result, Bits('0b010'))

    def test_xor_equal_length(self):
        with self.assertRaisesRegexp(BaseException, 'unequal length'):
            xor(Bits('0b1111'), Bits('0b11'))

    def test_expand_key_of_single_bit(self):
        result = expandKey(Bits('0b1'), 4)
        self.assertEquals(result, Bits('0b1111'))

    def test_expand_key_of_multiple_bits(self):
        result = expandKey(Bits('0b110'), 5)
        self.assertEquals(result, Bits('0b11011'))

    def test_expand_key_and_xor(self):
        result = expandKeyAndXor(Bits('0b11001100'), Bits('0b110'))
        self.assertEquals(result, Bits('0b00010111'))
        self.assertIs(result.pos, 0)

    def test_count_chars_ignore_case_in_string_upper_case(self):
        haystack = Bits(bytes="anadsgGfAbf")
        result = countCharsIgnoreCase(haystack, 'A');
        self.assertIs(result, 3)

    def test_count_chars_ignore_case_in_string_lower_case(self):
        haystack = Bits(bytes="anadsgGfAbf")
        result = countCharsIgnoreCase(haystack, 'a');
        self.assertIs(result, 3)

    def test_count_chars_ignore_case_in_string_no_match(self):
        haystack = Bits(bytes="aaaa")
        result = countCharsIgnoreCase(haystack, 'w');
        self.assertIs(result, 0)

    def test_count_chars_ignore_case_in_string_without_printable_char(self):
        haystack = Bits(hex="0x0010181f")
        result = countCharsIgnoreCase(haystack, 'a');
        self.assertIs(result, 0)

    def test_count_chars_ignore_case_in_string_mixed_printable_char(self):
        haystack = Bits(hex="0x00611018411f")
        result = countCharsIgnoreCase(haystack, 'a');
        self.assertIs(result, 2)

    def test_guess_key_for_single_byte_xor(self):
        text = Bits(bytes='Hello this is some english text')
        result = guessKeyForSingleByteXor(text)
        self.assertIs(result.int, 0)

    def test_guess_key_for_single_byte_xor_shifted(self):
        text = Bits(bytes='Hello this is some english text')
        result = guessKeyForSingleByteXor(expandKeyAndXor(text, Bits(hex="10")))
        self.assertIs(result.int, 16)

if __name__ == '__main__':
    unittest.main()

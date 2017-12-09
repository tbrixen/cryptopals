import unittest
from basic import xor, expandKey, expandKeyAndXor
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

if __name__ == '__main__':
    unittest.main()

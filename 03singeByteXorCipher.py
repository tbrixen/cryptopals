#!/usr/bin/env python

from lib.basic import expandKeyAndXor, guessKeyForSingleByteXor
from bitstring import Bits, BitArray, BitStream, ConstBitStream

def breakSingleKeyXor(input):
    winningChar = guessKeyForSingleByteXor(encrypted)

    #print "Maybe this is the solution using char %d: " % winningChar
    return expandKeyAndXor(encrypted, winningChar)

if __name__ == "__main__":
    encrypted = ConstBitStream(hex='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

    print breakSingleKeyXor(encrypted).bytes

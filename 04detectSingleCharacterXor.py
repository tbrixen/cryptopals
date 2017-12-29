#!/usr/bin/env python

from lib.basic import expandKeyAndXor, guessKeyForSingleByteXor, englishScore
from bitstring import Bits, BitArray, BitStream

if __name__ == "__main__":
    bestScore = 0
    winningChar = 0
    probablyTheString = ""
    with open ('04detectSingleCharacterXor.txt') as f:
        for line in f:
            print "Trying: " + line
            for c in range(255):
                encrypted = BitStream(hex=line)
                key = Bits(uint=c, length=8)
                decrypted = expandKeyAndXor(encrypted, key)
                curr_score = englishScore(decrypted)
                if curr_score > bestScore:
                    bestScore = curr_score
                    winningChar = c
                    probablyTheString = line

    encrypted = BitStream(hex=probablyTheString)
    print "Maybe this is the solution using char %d, of the string %s: " % (winningChar, probablyTheString)
    print expandKeyAndXor(encrypted, Bits(uint=winningChar, length=8)).bytes

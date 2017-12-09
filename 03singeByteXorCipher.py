#!/usr/bin/env python

from lib.basic import expandKeyAndXor, countCharsIgnoreCase
from bitstring import Bits, BitArray, BitStream, ConstBitStream

def englishScore(source):
    # Chars taken from the first two groups from studi made by Beker and
    # Piper. The number being multiplied is the probability of it occurring in
    # an english text. e.g. 'e' has the probability of 0.127. This I concluded
    # that if I saw an 'e' there was a higher probability that if I saw an 'r'.
    # Also see https://en.wikipedia.org/wiki/Etaoin_shrdlu
    score = 0
    scoreMap = {
        ' ': 127,
        'E': 127,
        'T': 91,
        'A': 82,
        'O': 75,
        'I': 70,
        'N': 67,
        'S': 63,
        'H': 61,
        'R': 60
    }
    for char, points in scoreMap.iteritems():
        score += countCharsIgnoreCase(source, char) * points

    return score

def getMostLikelyChar(encrypted):
    scoreMap = {}
    for c in range(255):
        char = Bits(uint=c, length=8)
        decrypted = expandKeyAndXor(encrypted, char)
        score = englishScore(decrypted)
        scoreMap[score] = char

    highestScore = sorted(scoreMap, reverse=True)[0]

    return scoreMap[highestScore]

def breakSingleKeyXor(input):
    winningChar = getMostLikelyChar(encrypted)

    #print "Maybe this is the solution using char %d: " % winningChar
    return expandKeyAndXor(encrypted, winningChar)

if __name__ == "__main__":
    encrypted = ConstBitStream(hex='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

    print breakSingleKeyXor(encrypted).bytes

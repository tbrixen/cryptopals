#!/usr/bin/env python

from bitstring import Bits, BitArray, BitStream, ConstBitStream

def xorWith(source, char):
    res = BitStream()
    key = Bits(uint=char, length=8)
    length = source.len;

    while (source.pos + 8 <= length):
        nextBits = source.read(8)
        res.append(nextBits ^ key)

    source.pos = 0
    return res

def englishScore(source):
    # Chars taken from the first two groups from studi made by Beker and
    # Piper. The number being multiplied is the probability of it occurring in
    # an english text. e.g. 'e' has the probability of 0.127. This I concluded
    # that if I saw an 'e' there was a higher probability that if I saw an 'r'.
    # Also see https://en.wikipedia.org/wiki/Etaoin_shrdlu
    noOfMostCommonChars = 0
    noOfMostCommonChars += numberOfChars(source, ' ')*127
    noOfMostCommonChars += numberOfChars(source, 'E')*127
    noOfMostCommonChars += numberOfChars(source, 'e')*127
    noOfMostCommonChars += numberOfChars(source, 'T')*91
    noOfMostCommonChars += numberOfChars(source, 't')*91
    noOfMostCommonChars += numberOfChars(source, 'a')*82
    noOfMostCommonChars += numberOfChars(source, 'A')*82
    noOfMostCommonChars += numberOfChars(source, 'O')*75
    noOfMostCommonChars += numberOfChars(source, 'o')*75
    noOfMostCommonChars += numberOfChars(source, 'I')*70
    noOfMostCommonChars += numberOfChars(source, 'i')*70
    noOfMostCommonChars += numberOfChars(source, 'N')*67
    noOfMostCommonChars += numberOfChars(source, 'n')*67
    noOfMostCommonChars += numberOfChars(source, 'S')*63
    noOfMostCommonChars += numberOfChars(source, 's')*63
    noOfMostCommonChars += numberOfChars(source, 'H')*61
    noOfMostCommonChars += numberOfChars(source, 'h')*61
    noOfMostCommonChars += numberOfChars(source, 'R')*60
    noOfMostCommonChars += numberOfChars(source, 'r')*60
    return noOfMostCommonChars

def numberOfChars(source, char):
    return len(list(source.findall(hex(ord(char)), bytealigned=True)))

def getMostLikelyChar(encrypted):
    bestScore = 0
    winningChar = 0
    for c in range(255):
        decrypted = xorWith(encrypted, c)
        curr_score = englishScore(decrypted)
        if curr_score > bestScore:
            bestScore = curr_score
            winningChar = c

    return winningChar

def breakSingleKeyXor(input):
    winningChar = getMostLikelyChar(encrypted)

    #print "Maybe this is the solution using char %d: " % winningChar
    return xorWith(encrypted, winningChar)



if __name__ == "__main__":
    encrypted = ConstBitStream(hex='1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

    print breakSingleKeyXor(encrypted).bytes

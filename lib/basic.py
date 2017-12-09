from bitstring import Bits, BitStream

def xor(a, b):
    if a.len != b.len:
        raise BaseException("Cannot XOR bitstrings of unequal length. Lengths was %d and %d" % (a.len, b.len))
    return a ^ b

def expandKeyAndXor(data, key):
    data = BitStream(data)
    key = BitStream(key)
    key = expandKey(key, data.length)
    res = BitStream()

    while key.pos + 8 <= key.length:
        res.append(xor(data.read(8), key.read(8)))

    return res

def expandKey(key, length):
    atLeast = (length / len(key)) + 1
    return (key*atLeast)[:length]

def countCharsIgnoreCase(source, char):
    a = source.bytes.count(char)
    b = source.bytes.count(char.swapcase())
    return  a + b

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

def guessKeyForSingleByteXor(encrypted):
    scoreMap = {}
    for c in range(255):
        char = Bits(uint=c, length=8)
        decrypted = expandKeyAndXor(encrypted, char)
        score = englishScore(decrypted)
        scoreMap[score] = char

    highestScore = sorted(scoreMap, reverse=True)[0]

    return scoreMap[highestScore]


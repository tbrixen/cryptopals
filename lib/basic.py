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

def canReadNextByte(data):
    return data.pos + 8 <= data.len

def canReadNextBytes(data, nBytes):
    return data.pos + nBytes*8 <= data.len

def countCharsIgnoreCase(source, char):
    a = source.bytes.count(char)
    b = source.bytes.count(char.swapcase())
    return a + b

def hammingDistance(a, b):
    return (a ^ b).count(1)

def readEveryXByte(data, x):
    result = BitStream()
    if not canReadNextByte(data):
        return result

    result.append(data.read(8))
    while canReadNextBytes(data, x):
        data.read((x-1)*8)
        result.append(data.read(8))

    return result

def readFromOffsetAndWithDistance(offset, blockSize, input):
    input.pos = offset*8
    firstBytesOfEachBlock = BitArray()
    while canReadNextBytes(input, blockSize):
        firstByteOfBlock = input.read(blockSize*8).read(8)
        firstBytesOfEachBlock.append(firstByteOfBlock)

    return ConstBitStream(firstBytesOfEachBlock)

def englishScore(source):
    # Chars taken from the first two groups from studi made by Beker and
    # Piper. The number being multiplied is the probability of it occurring in
    # an english text. e.g. 'e' has the probability of 0.127. This I concluded
    # that if I saw an 'e' there was a higher probability that if I saw an 'r'.
    # Also see https://en.wikipedia.org/wiki/Etaoin_shrdlu
    score = 0
    #scoreMap = {
    #    ' ': 1000,
    #    'E': 1202,
    #    'T': 910,
    #    'A': 812,
    #    'O': 768,
    #    'I': 731,
    #    'N': 695,
    #    'S': 628,
    #    'R': 602,
    #    'H': 592,
    #    'D': 432,
    #    'L': 398,
    #    'U': 288,
    #    'C': 271,
    #    'M': 271,
    #    'F': 230,
    #    'Y': 211,
    #    'W': 209,
    #    'G': 203,
    #    'P': 182,
    #    'B': 149,
    #    'V': 111,
    #    'K': 69,
    #    'X': 17,
    #    'Q': 11,
    #    'J': 10,
    #    'Z': 7,
    #    '?': 5,
    #    '/': 5,
    #    '!': 5,
    #    '"': 5,
    #    ',': 20,
    #    '.': 20,
    #    '\x00': -1000,
    #    '\x01': -1000,
    #    '\x02': -1000,
    #    '\x03': -1000,
    #    '\x04': -1000,
    #    '\x05': -1000,
    #    '\x06': -1000,
    #    '\x07': -1000,
    #    '\x08': -1000,
    #    '\x09': -1000,
    #    '\x10': -1000,
    #    '\x11': -1000,
    #    '\x12': -1000,
    #    '\x13': -1000,
    #    '\x14': -1000,
    #    '\x15': -1000,
    #    '\x16': -1000,
    #    '\x17': -1000,
    #    '\x18': -1000,
    #    '\x19': -1000,
    #}
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
        'R': 60,
        'D': 43,
        'L': 40,
        'U': 28,
        'M': 24,
        'W': 24,
        'F': 22,
        'Y': 20,
        'G': 20,
        'P': 19,
        'B': 15,
        'V': 10,
        'K': 8,
        'X': 2,
        'J': 2,
        'Q': 1
    }

    for char, points in scoreMap.iteritems():
        score += countCharsIgnoreCase(source, char) * points

    return score

def guessKeyForSingleByteXor(encrypted):
    scoreMap = {}
    for c in range(256):
        char = Bits(uint=c, length=8)
        decrypted = expandKeyAndXor(encrypted, char)
        score = englishScore(decrypted)
        scoreMap[score] = char

    highestScore = sorted(scoreMap, reverse=True)[0]

    return scoreMap[highestScore]


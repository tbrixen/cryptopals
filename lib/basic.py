from Crypto.Cipher import AES
from bitstring import Bits, BitStream, ConstBitStream
from collections import defaultdict

def xor(a, b):
    if a.len != b.len:
        raise BaseException("Cannot XOR bitstrings of unequal length. Lengths was %d and %d" % (a.len, b.len))
    return a ^ b

def expandKeyAndXor(data, key):
    data = BitStream(data)
    key = BitStream(key)
    key = expandKey(key, data.length)
    return data ^ key

def expandKey(key, length):
    k = key.bytes
    atLeast = (length / len(key)) + 1
    return (BitStream(bytes=k*atLeast))[:length]

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

def decrypt_aes_ecb(key, data):
    if key.length is not 128:
        raise ValueError("Key is not 128 bits. Input key size: %d bits" % key.length)
    if data.length % 128:
        raise ValueError("Data is not a multiple of 16 bytes. Data is %d bits", data.length)

    cipher = AES.new(key.bytes, AES.MODE_ECB)

    result = BitStream()
    while canReadNextBytes(data, 16):
        nextBytes = data.read(16*8)
        decrypted = cipher.decrypt(nextBytes.bytes)
        result += Bits(bytes=decrypted)

    return result

def ecb_score(bitstring):
    """ From bitstring (ConstBitStream) compute a score of the probablity of it
    being ecb encrypted with blocks of size 128 """
    counter = defaultdict(int)
    while canReadNextBytes(bitstring, 16):
        nextBytes = bitstring.read(16 * 8)
        counter[nextBytes] += 1

    total = 0
    for count in counter.itervalues():
        total += 2 ** count
    return total

def find_most_probable_ecb_encrypted(bitstring_list):
    """ From list of ConstBitStreams find the BitStrem with most repeating 128
    bits sequences """
    mostProbableData = ConstBitStream()
    highScore = 0
    for encryptedValue in bitstring_list:
        score = ecb_score(encryptedValue)
        if score > highScore:
            highScore = score
            mostProbableData = encryptedValue

    return mostProbableData

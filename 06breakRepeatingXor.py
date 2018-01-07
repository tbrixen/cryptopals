#!/usr/bin/env python
import sys, getopt
from lib.basic import hammingDistance, expandKeyAndXor, guessKeyForSingleByteXor, canReadNextBytes, readEveryXByte, englishScore
from bitstring import BitArray, ConstBitStream, BitStream, Bits

def break_cipher(input):
    keySizes = guessKeySizes(input)

    results = list()

    for keySize in keySizes:
        input.pos = 0

        key = BitStream()
        for pos in range(0, keySize):
            bytesToDecrypt = readFromOffsetAndWithDistance(pos, keySize, input)
            mostProbableKey = guessKeyForSingleByteXor(bytesToDecrypt)
            key.append(mostProbableKey)

        input.pos = 0
        key.pos = 0
        result = expandKeyAndXor(input, key)
        results.append((result, key))

    results.sort(key=lambda elm: englishScore(elm[0]), reverse=True)
    return results[0]

def readFromOffsetAndWithDistance(offset, blockSize, input):
    input.pos = offset*8
    return readEveryXByte(input, blockSize)

def guessKeySizes(input):
    normalizedDistances = list()

    for F in range(2, 41):
        keysize = F*8
        input.pos = 0
        running = 0
        number_of_blocks_to_read = 3
        for _ in range(0, number_of_blocks_to_read):
            part1 = input.read(keysize)
            part2 = input.read(keysize)
            input.pos -= keysize
            hd = hammingDistance(part1, part2)
            normalized = float(hd)
            running += normalized
        normalizedDistances.append((F, float(running) / float(F * 3)))

    keysizesToTry = set()
    numberOfKeysToTry = 5

    normalizedDistances.sort(key=lambda elm: elm[1])

    input.pos = 0
    return map((lambda x: x[0]), normalizedDistances[0: numberOfKeysToTry])

def main(argv):
    inputfile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inputfile=", "outputfile="])
    except getopt.GetoptError:
        print "breakingRepeatingKeyXor.py -i <inputfile> -o <outputfile>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "breakingRepeatingKeyXor.py -i <inputfile> -o <outputfile>"
            sys.exit(1)
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
             outputfile = arg

    base64encoded = ""
    f = open("06breakRepeatingXor.encrypted")
    for line in f.read().split('\n'):
        base64encoded += line
    f.close()

    result = break_cipher(ConstBitStream(bytes=base64encoded.decode('base64')))

    print result[0].bytes

if __name__ == "__main__":
    main(sys.argv[1:])

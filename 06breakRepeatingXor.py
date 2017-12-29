#!/usr/bin/env python
import sys, getopt
from lib.basic import hammingDistance, expandKeyAndXor, guessKeyForSingleByteXor, canReadNextBytes, readEveryXByte
from bitstring import BitArray, ConstBitStream, BitStream, Bits

def break_cipher(input):
    print "Starting to break"

    keySizes = guessKeySizes(input)
    print keySizes

    #keySizes = {24}

    for keySize in keySizes:
        input.pos = 0
        print "Trying keysize:", keySize

        key = BitStream()
        for pos in range(0, keySize):
            print "Guessing at pos", pos
            bytesToDecrypt = readFromOffsetAndWithDistance(pos, keySize, input)
            mostProbableKey = guessKeyForSingleByteXor(bytesToDecrypt)
            key.append(mostProbableKey)

        print "Key is probably:", key.hex

        input.pos = 0
        key.pos = 0
        result = expandKeyAndXor(input, key)
        print "Bytes"
        print result.bytes
        print "Hex"
        print result.hex


def readFromOffsetAndWithDistance(offset, blockSize, input):
    input.pos = offset*8
    return readEveryXByte(input, blockSize)

def guessKeySizes(input):
    normalizedDistances = {}

    for keysize in range(2,41):
        input.pos = 0
        running = 0
        for _ in range(0,3):
            part1 = input.read(keysize)
            part2 = input.read(keysize)
            hd = hammingDistance(part1, part2)
            normalized = float(hd) / float(keysize)
            #print "HD:", hd, "keysize", keysize, "normalized", normalized
            running += normalized
        normalizedDistances[float(running)/float(3)] = keysize

    keysizesToTry = set()
    numberOfKeysToTry = 5

    for i, key in enumerate(sorted(normalizedDistances.iterkeys())):
        if i < numberOfKeysToTry:
            keysizesToTry.add(normalizedDistances[key])
        #print "%s, %s, %d" % (key, normalizedDistances[key], i)

    input.pos = 0
    return keysizesToTry

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

    break_cipher(ConstBitStream(bytes=base64encoded.decode('base64')))

if __name__ == "__main__":
    main(sys.argv[1:])

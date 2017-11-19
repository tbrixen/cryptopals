#!/usr/bin/env python
import sys, getopt
from bitstring import BitArray, ConstBitStream

TEXT_TO_ENCRYPT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

KEY = "ICE"

TEST_OUTPUT = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def expand_key(key, length):
    atLeast = (length / len(key)) + 1
    return (key*atLeast)[:length]

def xor(plaintext, key):
    p = ConstBitStream(bytes=plaintext)
    k = ConstBitStream(bytes=key)
    k = expand_key(k, p.length)
    res = BitArray()

    while k.pos + 8 <= k.length:
        res.append(p.read(8) ^ k.read(8))

    return res.hex

def main(argv):
    inputfile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inputfile=", "outputfile="])
    except getopt.GetoptError:
        print "implementingRepeatingKeyXor.py -i <inputfile> -o <outputfile>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print "implementingRepeatingKeyXor.py -i <inputfile> -o <outputfile>"
            sys.exit(1)
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
             outputfile = arg


    if len(inputfile) != 0:
        print "Trying to read", inputfile
        toEncrypt = BitArray(filename=inputfile).hex

        result = xor(toEncrypt, KEY)

        f = open(outputfile, "w")
        f.write(result.decode('hex').encode('base64'))
        f.close()
    else:
        run_test()

def run_test():
    result = xor(TEXT_TO_ENCRYPT, KEY)
    if result == TEST_OUTPUT:
        print "WIN"
    else:
        print "Failed"
        print "Should be: \t" + TEST_OUTPUT
        print "But was : \t" + result


if __name__ == "__main__":
    main(sys.argv[1:])

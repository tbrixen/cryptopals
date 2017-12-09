#!/usr/bin/env python
import sys, getopt
from lib.basic import expandKeyAndXor
from bitstring import BitArray, ConstBitStream

TEXT_TO_ENCRYPT = ConstBitStream(bytes="""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal""")

KEY = ConstBitStream(bytes="ICE")

TEST_OUTPUT = ConstBitStream(hex="0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")

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
        toEncrypt = ConstBitArray(filename=inputfile)

        result = xor(toEncrypt, KEY)

        f = open(outputfile, "w")
        f.write(result.decode('hex').encode('base64'))
        f.close()
    else:
        run_test()

def run_test():
    result = expandKeyAndXor(TEXT_TO_ENCRYPT, KEY)
    if result == TEST_OUTPUT:
        print "WIN"
    else:
        print "Failed"
        print "Should be: \t" + TEST_OUTPUT
        print "But was : \t" + result


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python
import sys, getopt
from cp.basic import expand_key_and_xor

TEXT_TO_ENCRYPT = b"""Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

KEY = b"ICE"

TEST_OUTPUT = bytes.fromhex("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f")

def main(argv):
    inputfile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inputfile=", "outputfile="])
    except getopt.GetoptError:
        print("implementingRepeatingKeyXor.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("implementingRepeatingKeyXor.py -i <inputfile> -o <outputfile>")
            sys.exit(1)
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
             outputfile = arg


    if len(inputfile) != 0:
        print("Trying to read", inputfile)
        toEncrypt = ConstBitArray(filename=inputfile)

        result = xor(toEncrypt, KEY)

        f = open(outputfile, "w")
        f.write(result.decode('hex').encode('base64'))
        f.close()
    else:
        output_challenge_text()

def output_challenge_text():
    result = expand_key_and_xor(TEXT_TO_ENCRYPT, KEY)

    output_message = ("SET 01 CHALLENGE 05: Implement repeating-key XOR\n"
                      "    Plaintext:    {}\n"
                      "    Key:          {}\n"
                      "    Result (hex): {}")

    print(output_message.format(TEXT_TO_ENCRYPT.decode(), KEY.decode(), result.hex()))

if __name__ == "__main__":
    main(sys.argv[1:])

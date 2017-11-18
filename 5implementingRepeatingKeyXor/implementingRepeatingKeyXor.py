#!/usr/bin/env python

TEXT_TO_ENCRYPT = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

KEY = "ICE"

TEST_OUTPUT = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

def xorEqualSizeInts(plaintext, key):
    return plaintext ^ key

def getHexStringFromInt(input):
    return hex(input)[2:-1]

def getIntFromHex(hexx):
    return int(hexx, 16)

def expand_key(key, length):
    atLeast = (length / len(key)) + 1
    return (key*atLeast)[:length]

def xor(plaintext, key):
    expanded_key = expand_key(key, len(plaintext))
    xored = getIntFromHex(plaintext.encode('hex')) ^ getIntFromHex(expanded_key.encode('hex'))
    return "0" + getHexStringFromInt(xored)

if __name__ == "__main__":
    result = xor(TEXT_TO_ENCRYPT, KEY)
    if result == TEST_OUTPUT:
        print "WIN"
    else:
        print "Failed"
        print "Should be: \t" + TEST_OUTPUT
        print "But was : \t" + result

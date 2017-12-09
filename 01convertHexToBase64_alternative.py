from bitstring import ConstBitStream
# PymodeVirtualenv /Users/tbrixen/tbrpyenv/

BASE64SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def getBase64Char(codePoint):
    if codePoint >= 64 or codePoint < 0:
        raise ValueError('Codepoint is outside of range: ' + str(codePoint))
    return BASE64SET[codePoint]

def hexStringToBase64(source):
    s = ConstBitStream(hex=source)
    result = "";

    if s.length % 6 != 0:
        raise ValueError('Implementation does not support padding. Length of input must be divisible by 6. Length was ' + str(s.length))

    while(s.pos + 6 <= s.length):
        result += getBase64Char(s.read('uint:6'))
    return result


if __name__ == "__main__":
    source = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    shouldProduce = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    result = hexStringToBase64(source)
    if (result == shouldProduce):
        print "win"
    else:
        print "Sorry, it did not match:"
        print "Was: \t\t\t\t" + result
        print "Should be: \t" + shouldProduce



#!/usr/bin/env python

BASE64SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
def getBase64Char(codePoint):
    if codePoint >= 64 or codePoint < 0:
        raise ValueError('Codepoint is outside of range: ' + str(codePoint))
    return BASE64SET[codePoint]

def hexStringToBase64(hexString):
    src = int(hexString, 16)
    result = ""
    SIX_BIT_MASK = int('111111', 2)

    while(True):
        if src == 0:
            break
        codePoint = src & SIX_BIT_MASK
        result = getBase64Char(codePoint) + result
        src >>= 6

    return result

if __name__ == "__main__":
    source = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    shouldProduce = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
    result = hexStringToBase64(source)
    if (result == shouldProduce):
        print("win")
    else:
        print("Sorry, it did not match:")
        print("Was: \t\t\t\t" + result)
        print("Should be: \t" + shouldProduce)



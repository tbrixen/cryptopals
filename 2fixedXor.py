#!/usr/bin/env python

def getHexstringFromInt(input):
    return hex(input)[2:-1]

if __name__ == "__main__":
    source =     int("1c0111001f010100061a024b53535009181c", 16)
    xored_with = int("686974207468652062756c6c277320657965", 16)
    should_be_result = "746865206b696420646f6e277420706c6179"
    xored = getHexstringFromInt(source ^ xored_with)
    if xored == should_be_result:
        print "WIN"
    else :
        print "Failed"
        print "Should be: \t" + should_be_result
        print "But was : \t" + xored

from bitstring import Bits, BitStream

def xor(a, b):
    if a.len != b.len:
        raise BaseException("Cannot XOR bitstrings of unequal length. Lengths was %d and %d" % (a.len, b.len))
    return a ^ b

def expandKeyAndXor(data, key):
    data = BitStream(data)
    key = BitStream(key)
    key = expandKey(key, data.length)
    res = BitStream()

    while key.pos + 8 <= key.length:
        res.append(xor(data.read(8), key.read(8)))

    return res

def expandKey(key, length):
    atLeast = (length / len(key)) + 1
    return (key*atLeast)[:length]

def countCharsIgnoreCase(source, char):
    a = source.bytes.count(char)
    b = source.bytes.count(char.swapcase())
    return  a + b


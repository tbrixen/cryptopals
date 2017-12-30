from lib.basic import canReadNextBytes, decrypt_aes_ecb
from bitstring import ConstBitStream
from collections import defaultdict

def ecb_score(bitstring):
    """ From bitstring (ConstBitStream) compute a score of the probablity of it
    being ecb encrypted with blocks of size 128 """
    counter = defaultdict(int)
    while canReadNextBytes(bitstring, 16):
        nextBytes = bitstring.read(16 * 8)
        counter[nextBytes] += 1

    total = 0
    for count in counter.itervalues():
        total += 2 ** count
    return total

def find_most_probable_ecb_encrypted(bitstring_list):
    """ From list of ConstBitStreams find the BitStrem with most repeating 128
    bits sequences """
    mostProbableData = ConstBitStream()
    highScore = 0
    for encryptedValue in bitstring_list:
        score = ecb_score(encryptedValue)
        if score > highScore:
            highScore = score
            mostProbableData = encryptedValue

    return mostProbableData

def main():
    data = list()
    f = open("08detectAesInEcbMode.txt")
    for line in f.read().split('\n'):
        data.append(ConstBitStream(hex=line))
    f.close()

    mostProbable = find_most_probable_ecb_encrypted(data)
    print mostProbable.hex

if __name__ == "__main__":
    main()


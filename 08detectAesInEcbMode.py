from lib.basic import canReadNextBytes
from bitstring import ConstBitStream
from collections import defaultdict

def ecb_score(data):
    counter = defaultdict(int)
    while canReadNextBytes(data, 16):
        nextBytes = data.read(16*8)
        counter[nextBytes] += 1

    total = 0
    for count in counter.itervalues():
        total += 2 ** count
    return total

def main():
    scores = {}
    f = open("08detectAesInEcbMode.txt")
    for line in f.read().split('\n'):
        score = ecb_score(ConstBitStream(hex=line))
        scores[line] = score
    f.close()

if __name__ == "__main__":
    main()


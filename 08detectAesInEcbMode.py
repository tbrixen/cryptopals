from lib.basic import canReadNextBytes, decrypt_aes_ecb
from bitstring import ConstBitStream
from collections import defaultdict

def ecb_score(data):
    counter = defaultdict(int)
    while canReadNextBytes(data, 16):
        nextBytes = data.read(16 * 8)
        counter[nextBytes] += 1

    total = 0
    for count in counter.itervalues():
        total += 2 ** count
    return total

def find_most_probable_ecb_encrypted(data):
    data_to_score_map = {}
    for encrypted_value in data:
        score = ecb_score(encrypted_value)
        data_to_score_map[encrypted_value] = score

    bestScore = 0
    bestData = ConstBitStream()
    for encrypted_value, count in data_to_score_map.items():
        if count > bestScore:
            bestScore = count
            bestData = encrypted_value

    return bestData

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


from lib.basic import find_most_probable_ecb_encrypted
from bitstring import ConstBitStream

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


from lib.basic import canReadNextBytes, decrypt_aes_ecb
from bitstring import ConstBitStream

def ecb_score(data):
    return 42

def main():
    key = ConstBitStream(bytes="YELLOW SUBMARINE")

    scores = {}
    f = open("08detectAesInEcbMode.txt")
    for line in f.read().split('\n'):
        print line
        score = ecb_score(ConstBitStream(hex=line))
        scores[line] = score
    f.close()

    print scores

if __name__ == "__main__":
    main()


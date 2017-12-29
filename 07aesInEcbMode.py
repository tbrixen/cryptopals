from lib.basic import canReadNextBytes, decrypt_aes_ecb
from bitstring import ConstBitStream

def main():
    key = ConstBitStream(bytes="YELLOW SUBMARINE")

    base64encoded = ""
    f = open("07AESinECBmode.encrypted")
    for line in f.read().split('\n'):
        base64encoded += line
    f.close()

    result = decrypt_aes_ecb(key, ConstBitStream(bytes=base64encoded.decode('base64')))

    print result.bytes

if __name__ == "__main__":
    main()

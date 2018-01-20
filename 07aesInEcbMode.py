from cp.basic import decrypt_aes_ecb
import base64

def main():
    key = b"YELLOW SUBMARINE"

    base64encoded = ""
    f = open("07aesInECBmode.encrypted")
    for line in f.read().split('\n'):
        base64encoded += line
    f.close()

    result = decrypt_aes_ecb(key, base64.b64decode(base64encoded))

    output_message = """SET 01 CHALLENGE 07: AES in ECB mode
    Plaintext:       {}"""

    print(output_message.format( \
        result.decode()))

if __name__ == "__main__":
    main()

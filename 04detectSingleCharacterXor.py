#!/usr/bin/env python
from cp.basic import break_single_key_xor, english_score

def main():
    lines = list()
    with open ('04detectSingleCharacterXor.txt') as f:
        for line in f:
            lines.append(bytes.fromhex(line.strip()))

    lines.sort(key=lambda x: english_score(x), reverse=True)
    ciphertext = lines[0]

    result = break_single_key_xor(ciphertext)

    output_message = """SET 01 CHALLENGE 04: Detect single-character XOR
    Hex source: {}
    Key (hex):  {}
    Decrypted:  {}"""

    print(output_message.format(\
        ciphertext.hex(), \
        result['key'].hex(), \
        result['plaintext'].decode("UTF-8")))

if __name__ == "__main__":
    main()

#!/usr/bin/env python
from cp.basic import break_single_key_xor

if __name__ == "__main__":
    encrypted = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    result = break_single_key_xor(bytes.fromhex(encrypted))

    output_message = """SET 01 CHALLENGE 03: Single-byte XOR Cipher
    Hex source:  {}
    Result:      {}"""

    print(output_message.format(encrypted, result))

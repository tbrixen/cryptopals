#!/usr/bin/env python
from cp.basic import xor

if __name__ == "__main__":
    a = '1c0111001f010100061a024b53535009181c'
    b = '686974207468652062756c6c277320657965'
    result = xor(bytes.fromhex(a), bytes.fromhex(b))

    output_message = """SET 01 CHALLENGE 02: Fixed byte XOR
    First buffer:   {}
    Second buffer:  {}
    Result:         {}"""

    print(output_message.format(a, b, result.hex()))

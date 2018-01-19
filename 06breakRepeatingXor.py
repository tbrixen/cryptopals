#!/usr/bin/env python
import sys, getopt
import base64
from cp.basic import hamming_distance, expand_key_and_xor, guess_key_for_single_byte_xor, english_score

def break_cipher(encrypted):
    key_sizes = guess_key_size(encrypted)

    results = list()
    for key_size in key_sizes:
        transposed_blocks = transpose(encrypted, key_size)
        key = bytearray()
        for block in transposed_blocks:
            most_probable_key = guess_key_for_single_byte_xor(block)
            key.append(most_probable_key[0])

        result = expand_key_and_xor(encrypted, key)
        results.append({'plaintext': result, 'key': key})

    results.sort(key=lambda x: english_score(x['plaintext']), reverse=True)
    return results[0]

def transpose(inp, block_size):
    transposed_blocks = list()
    for _ in range(block_size):
        transposed_blocks.append(bytearray())

    for idx in range(len(inp)):
        i = idx % block_size
        transposed_blocks[i].append(inp[idx])

    return transposed_blocks

def guess_key_size(inp):
    normalized_distances = list()

    for keysize in range(2, 41):
        running = 0
        number_of_blocks_to_read = 3
        for count in range(0, number_of_blocks_to_read):
            pos = count * keysize
            part1 = inp[pos : pos + keysize]
            part2 = inp[pos + keysize  : pos + 2*keysize]
            hd = hamming_distance(part1, part2)
            normalized = float(hd)
            running += normalized
        normalized_distances.append((keysize, float(running) / float(keysize * 3)))

    keysizesToTry = set()
    numberOfKeysToTry = 5

    normalized_distances.sort(key=lambda elm: elm[1])

    return map((lambda x: x[0]), normalized_distances[0: numberOfKeysToTry])

def main(argv):
    inputfile=''
    outputfile=''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inputfile=", "outputfile="])
    except getopt.GetoptError:
        print("breakingRepeatingKeyXor.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("breakingRepeatingKeyXor.py -i <inputfile> -o <outputfile>")
            sys.exit(1)
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
             outputfile = arg

    base64encoded = ""
    f = open("06breakRepeatingXor.encrypted")
    for line in f.read().split('\n'):
        base64encoded += line
    f.close()

    result = break_cipher(base64.b64decode(base64encoded))

    output_message = """SET 01 CHALLENGE 06: Break repeating-charecter XOR
    Key (hex): {}
    Key      : {}
    Plaintext: {}"""

    print(output_message.format(\
        result['key'].hex(),
        result['key'].decode("UTF-8"),
        result['plaintext'].decode("UTF-8")))

if __name__ == "__main__":
    main(sys.argv[1:])

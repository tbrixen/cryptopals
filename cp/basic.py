from collections import defaultdict
from Crypto.Cipher import AES

def xor(a, b):
    if len(a) != len(b):
        raise BaseException("Cannot XOR bitstrings of unequal length. Lengths was %d and %d" % (len(a), len(b)))
    return bytearray([x ^ y for x, y in zip(a, b)])

def expand_key_and_xor(data, key):
    key = expand_key(key, len(data))
    return xor(data, key)

def expand_key(key, length):
    return (key * length)[:length]

def hamming_distance(a, b):
    c = xor(a, b)
    return binary(c).count('1')

def binary(input):
    return bin(int(input.hex(), 16))[2:]

def english_score(source):
    # Chars taken from the first two groups from studi made by Beker and
    # Piper. The number being multiplied is the probability of it occurring in
    # an english text. e.g. 'e' has the probability of 0.127. This I concluded
    # that if I saw an 'e' there was a higher probability that if I saw an 'r'.
    # Also see https://en.wikipedia.org/wiki/Etaoin_shrdlu
    scores = {
        ' ': 127,
        'E': 127,
        'T': 91,
        'A': 82,
        'O': 75,
        'I': 70,
        'N': 67,
        'S': 63,
        'H': 61,
        'R': 60,
        'D': 43,
        'L': 40,
        'U': 28,
        'M': 24,
        'W': 24,
        'F': 22,
        'Y': 20,
        'G': 20,
        'P': 19,
        'B': 15,
        'V': 10,
        'K': 8,
        'X': 2,
        'J': 2,
        'Q': 1
    }
    score = 0
    score_map = defaultdict(int, **scores)

    for char_point in source:
        char = chr(char_point).upper()
        score += score_map[char]

    return score

def guess_key_for_single_byte_xor(encrypted):
    score_map = dict()
    for c in range(256):
        key_candidate = bytes([c])
        decrypted = expand_key_and_xor(encrypted, key_candidate)
        score = english_score(decrypted)
        score_map[score] = key_candidate

    highest_score = sorted(score_map, reverse=True)[0]

    return score_map[highest_score]

def break_single_key_xor(encrypted):
    winningChar = guess_key_for_single_byte_xor(encrypted)
    plaintext = expand_key_and_xor(encrypted, winningChar)
    return {'key': winningChar, 'plaintext': plaintext}

def decrypt_aes_ecb(key, data):
    if len(key) is not 16:
        raise ValueError("Key is not 16 bytes. Input key size: %d bytes" % len(key))
    if len(data) % 16:
        raise ValueError("Data is not a multiple of 16 bytes. Data is %d bytes", len(data))

    cipher = AES.new(key, AES.MODE_ECB)

    result = bytearray()
    for block_index in range(0, len(data), 16):
        next_bytes = data[block_index : block_index + 16]
        decrypted = cipher.decrypt(next_bytes)
        result.extend(decrypted)

    return result

def ecb_score(bitstring):
    """ From bitstring (ConstBitStream) compute a score of the probablity of it
    being ecb encrypted with blocks of size 128 """
    counter = defaultdict(int)

    for block_index in range(0, len(bitstring), 16):
        next_bytes = bitstring[block_index : block_index + 16]
        counter[next_bytes] += 1

    total = 0
    for count in counter.values():
        total += 2 ** count
    return total

def find_most_probable_ecb_encrypted(bitstring_list):
    """ From list of ConstBitStreams find the BitStrem with most repeating 128
    bits sequences """
    mostProbableData = bytes()
    highScore = 0
    for encryptedValue in bitstring_list:
        score = ecb_score(encryptedValue)
        if score > highScore:
            highScore = score
            mostProbableData = encryptedValue

    return mostProbableData

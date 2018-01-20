from cp.basic import find_most_probable_ecb_encrypted

def main():
    data = list()
    f = open("08detectAesInEcbMode.txt")
    for line in f.read().split('\n'):
        data.append(bytes.fromhex(line))
    f.close()

    most_probable = find_most_probable_ecb_encrypted(data)

    output_message = """SET 01 CHALLENGE 08: Detect AES in ECB mode
    Most probable ECB encrypted ciphertext (hex):    {}"""

    print(output_message.format(\
        most_probable.hex()))

if __name__ == "__main__":
    main()


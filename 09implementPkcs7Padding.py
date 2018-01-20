from cp.blockcrypto import pkcs7_pad

def main():
    source = b"YELLOW SUBMARINE"
    block_size = 20
    result = pkcs7_pad(source, block_size)

    output_message = """SET 02 Challenge 01: Pkcs7 padding
    Input:         {}
    Input (hex):   {}
    Block size:    {}
    Result (hex):  {}"""

    print(output_message.format(\
        source.decode(),
        source.hex(),
        block_size,
        result.hex()))

if __name__ == "__main__":
    main()


def pkcs7_pad(data, blocksize):
    result = bytearray(data)
    padding_size = blocksize - (len(data) % blocksize)

    if padding_size is 0:
        padding_size = blocksize
    padding = [padding_size for _ in range(padding_size)]
    result.extend(padding)

    return result

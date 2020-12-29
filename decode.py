import struct
import sys


def byte_arr_to_number(arr, byte_num):
    number = 0
    for n in range(byte_num):
        number += (arr[n] << 8 * (byte_num - n - 1))

    return number


def decode(input_file, output_file):
    data = open(input_file, "rb").read()
    file = open(output_file, "wb")

    buffer = "".encode()

    i = 2
    byte_len, lookahead_bytes = struct.unpack('BB', data[:i])

    while i < len(data):
        *byte_arr, letter = struct.unpack('B' * (byte_len+1), data[i:i+byte_len+1])

        offset_and_length = byte_arr_to_number(byte_arr, byte_len)

        offset = offset_and_length >> lookahead_bytes
        length = offset_and_length - offset * (2**lookahead_bytes)

        if offset > len(buffer):
            print("Err! Input file can't be decoded")
            return

        if offset > 0:
            buffer += buffer[-offset: -offset + length]
        buffer += letter.to_bytes(1, 'big')
        i += 3
    file.write(buffer)


def main():
    decode(*sys.argv[1:])


if __name__ == "__main__":
    main()
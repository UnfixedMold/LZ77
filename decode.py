import struct
import sys


def main():

    [_, input_file, output_file] = sys.argv

    data = open(input_file, "rb").read()
    file = open(output_file, "wb")

    buffer = "".encode()

    lookahead_bytes, *_ = struct.unpack('H', data[:2])
    i = 2

    while i < len(data):
        offset_and_length, letter = struct.unpack('HB', data[i:i+3])
        offset = offset_and_length >> lookahead_bytes
        length = offset_and_length - offset * (2**lookahead_bytes)

        if offset > len(buffer):
            print("Err! Input file can't be decoded")
            return

        if offset > 0:
            buffer += buffer[-offset: -offset + length]
        buffer += letter.to_bytes(1,'big')
        i += 3
    file.write(buffer)


if __name__ == "__main__":
    main()
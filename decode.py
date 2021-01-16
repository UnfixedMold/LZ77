import struct
import sys


def main():
    [_, input_file, output_file] = sys.argv

    data = open(input_file, "rb").read()
    file = open(output_file, "wb")

    buffer = "".encode()
    i = 0
    lookahead_bytes, *_ = struct.unpack('H', data[:2])
    search_bytes, *_ = struct.unpack('H', data[2:4])
    data_string = ""
    for k in data[4:]:
        data_string += "{:08b}".format(k)

    while i + 8 < len(data_string):

        offset = int(data_string[i:i + search_bytes], 2)
        length = int(data_string[i + search_bytes:i + search_bytes + lookahead_bytes], 2)
        letter = int(data_string[i + search_bytes + lookahead_bytes:i + search_bytes + lookahead_bytes + 8], 2)

        if offset > len(buffer):
            print("Err! Input file can't be decoded")
            return

        if offset > 0:
            buffer += buffer[-offset: -offset + length]
        buffer += letter.to_bytes(1, 'big')

        i += search_bytes + lookahead_bytes + 8
    file.write(buffer)


if __name__ == "__main__":
    main()

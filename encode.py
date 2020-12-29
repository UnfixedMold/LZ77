import struct
import sys
import os
import math


def find_match(search_buf, lookahead_buf, max_match_depth):

    sl = len(search_buf)
    lal = len(lookahead_buf)

    buffers = search_buf + lookahead_buf

    if sl == 0:
        return 0, 0, lookahead_buf[0]

    if lal == 0:
        return -1, -1, ""

    best_match = ""
    best_length = 0
    best_it = 0
    max_it = 0
    i = 0

    while i < sl:

        if max_match_depth and max_it >= int(max_match_depth):
            break

        length = 0
        match_find = False

        while buffers[i + length] == buffers[sl + length]:
            match_find = True
            length = length + 1
            if len(best_match) < length:
                best_length = length
                best_match = buffers[sl:sl + length]
                best_it = i

            if sl + length == len(buffers):
                best_length = best_length - 1
                return sl - best_it, best_length, lookahead_buf[best_length]
            if i + length >= sl:
                return sl - best_it, best_length-1, lookahead_buf[best_length-1]
        if match_find:
            max_it = max_it + 1
        i = i + 1
    if best_length == 0 or best_length == 1:
        return 0, 0, lookahead_buf[0]

    return sl - best_it, best_length, lookahead_buf[best_length]


def number_to_byte_arr(number, byte_num):
    return [(number >> 8 * n) & 0xff for n in reversed(range(byte_num))]


def encode(file_to_read, file_to_write, search_bytes, lookahead_bytes, max_match_depth=None):

    search_bytes = int(search_bytes)
    lookahead_bytes = int(lookahead_bytes)

    byte_len = math.ceil((search_bytes + lookahead_bytes)/8)

    data = open(file_to_read, "rb").read()
    file = open(file_to_write, "wb")

    search_len = (2**search_bytes) - 1
    lookahead_len = (2**lookahead_bytes) - 1

    search_iterator = 0
    lookahead_it = 0

    file.write(struct.pack('BB', byte_len, lookahead_bytes))

    while lookahead_it in range(len(data)):
        search_buf = data[search_iterator:lookahead_it]
        lookahead_buf = data[lookahead_it:lookahead_it + lookahead_len]

        (offset, length, symbol) = find_match(search_buf, lookahead_buf, max_match_depth)
        file.write(struct.pack("B" * (byte_len + 1), *number_to_byte_arr((offset << lookahead_bytes) + length, byte_len), symbol))
        lookahead_it += length + 1

        if lookahead_it >= search_len:
            search_iterator = lookahead_it - search_len


def test():

    [_, file, *_] = sys.argv

    test_dir = "./test"

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    file_dir = '{test_dir}/{file}'

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    for i in range(1, 16):
        j = 16-i
        encode(file, '{file_dir}/{i}_{j}', i, j)
        print('{i}_{j} completed!')


def main():

    encode(*sys.argv[1:])
    # test()


if __name__ == "__main__":
    main()

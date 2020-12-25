import struct
import sys
import os


def find_match(search_buf, lookahead_buf):

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

    for i in range(sl):
        length = 0
        while buffers[i + length] == buffers[sl + length]:
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

    if best_length == 0 or best_length == 1:
        return 0, 0, lookahead_buf[0]

    return sl - best_it, best_length, lookahead_buf[best_length]


def encode(file_to_read, file_to_write, search_bytes, lookahead_bytes):

    search_bytes = int(search_bytes)
    lookahead_bytes = int(lookahead_bytes)

    if (search_bytes + lookahead_bytes) > 16:
        print("Err! Sum of search window and match window can't be greater than 16!")

    data = open(file_to_read, "rb").read()
    file = open(file_to_write, "wb")

    search_len = (2**search_bytes) - 1
    lookahead_len = (2**lookahead_bytes) - 1

    search_iterator = 0
    lookahead_it = 0

    file.write(struct.pack('H', lookahead_bytes))

    while lookahead_it in range(len(data)):
        search_buf = data[search_iterator:lookahead_it]
        lookahead_buf = data[lookahead_it:lookahead_it + lookahead_len]

        (offset, length, symbol) = find_match(search_buf, lookahead_buf)

        file.write(struct.pack('Hs', (offset << lookahead_bytes) + length, chr(symbol).encode()))

        lookahead_it += length + 1

        if lookahead_it >= search_len:
            search_iterator = lookahead_it - search_len


def test():

    [_, file, *_] = sys.argv

    test_dir = "./test"

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    file_dir = f'{test_dir}/{file}'

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    for i in range(1, 16):
        j = 16-i
        encode(file, f'{file_dir}/{i}_{j}', i, j)
        print(f'{i}_{j} completed!')


def main():

    encode(*sys.argv[1:])
    # test()


if __name__ == "__main__":
    main()

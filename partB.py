import sys
from partA import Tokenizer


def count_common_tokens(file1, file2):
    t = Tokenizer()
    common_count = 0
    token_list_file_1 = {x for x in t.tokenize(file1)}
    for token in t.yield_tokens(file2):
        if token in token_list_file_1:
            common_count += 1
            token_list_file_1.remove(token)  # avoids duplicate counting of the same word in both documents
    print(common_count)


def main():
    if len(sys.argv) != 3:
        print("Error: User forgot to enter two files in the command line.")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    count_common_tokens(file1, file2)


if __name__ == "__main__":
    main()

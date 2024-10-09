import collections
import sqlite3
import os




class TokenTable:

    def __init__(self):
        self.conn = sqlite3.connect("tokenStore.db")

        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE Tokens(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE,
                freq INTEGER );""")

        self.conn.commit()

        cursor.close()

    def insert(self, word: str):
        cursor = self.conn.cursor()

        cursor.execute("""INSERT INTO Tokens (word, freq) VALUES (?, 1) ON CONFLICT(word) DO UPDATE SET freq = freq + 1""", word)

        cursor.close()

    def queryAll(self):
        cursor = self.conn.cursor()
        for token in cursor.execute("""SELECT * FROM tokens"""):
            yield token
        cursor.close()

    def resetTable(self):
        cursor = self.conn.cursor()
        cursor.execute("""DELETE FROM tokens""")
        cursor.close()


class Tokenizer:

    def yield_line_from_file(self, text_file_path: str):
        try:
            with open(text_file_path) as infile:
                for line in infile:
                    yield line.lower()
        except FileNotFoundError:
            return []

    def get_token(self, line: str):
        # for line in self.yield_line_from_file("test1.txt"):
        word = ""
        for c in line:
            if c.isalnum():
                word += c
            else:
                if len(word):
                    yield word
                    word = ""

    def yield_tokens(self, text_file_path: str):
        for line in self.yield_line_from_file(text_file_path):
            for token in self.get_token(line):
                yield token

    def tokenize(self, text_file_path: str):
        tokens = []
        for line in self.yield_line_from_file(text_file_path):
            for token in self.get_token(line):
                tokens.append(token)
        return tokens

    def compute_word_frequencies(self, tokens: list[str]):
        return collections.Counter(tokens)

    def print_frequencies(self, mappedFrequencies: dict[str: int]):
        for (k,v) in {k: v for k, v in sorted(mappedFrequencies.items(), key=lambda item: item[1], reverse=True)}.items():  # code from https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
            print(f"{k}\t{v}")
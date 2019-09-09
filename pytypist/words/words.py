import os
from typing import List


def collect_words() -> List[str]:
    dire_name = os.path.dirname(os.path.realpath(__file__))
    file_name = "words.txt"
    with open(file_name, "r") as target_file:
        contents = target_file.read()
    words = [w.strip() for w in contents.split("\n")]
    return words


def collect_words_containing(target_characters: str) -> List[str]:
    words = collect_words()
    words_subset = []
    for word in words:
        has_target_characters = True
        for char in word:
            if char not in target_characters:
                has_target_characters = False
        if has_target_characters:
            words_subset.append(word)

    return words_subset


def main():
    words = collect_words_containing("asdfjkl;")
    print(words)


if __name__ == "__main__":
    main()
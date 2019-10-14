from pytypist.words import (
    collect_words_containing,
    capitalize,
    collect_words_starting_with,
    collect_words_ending_with,
)


def only_characters_included(words, characters):
    for word in words:
        for char in word:
            if char not in characters:
                return False  # pragma: no cover
    return True


def has_required_characters(words, characters):
    for word in words:
        includes_character = False
        for char in characters:
            if char in word:
                includes_character = True
        if not includes_character:
            return False  # pragma: no cover

    return True


def test_collect_words():
    characters = "asdf"
    words = collect_words_containing(characters)
    assert len(words) > 0
    assert only_characters_included(
        words, characters
    )


def test_collect_words_must_contain():
    characters = "asdf"
    required = "as"
    words = collect_words_containing(characters, must_contain=required)
    print(words)
    assert len(words) > 0
    assert only_characters_included(
        words, characters
    )
    assert has_required_characters(
        words, required
    )


def test_capitalize():
    assert capitalize("this") == "This"
    assert capitalize("THAT") == "That"
    assert capitalize("MoRe") == "More"


def test_collect_words_starting_with():
    words = collect_words_starting_with("a")
    for word in words:
        assert word[0] == "a"
    words = collect_words_starting_with("Sta")
    for word in words:
        assert word[:3] == "sta"


def test_collect_words_ending_with():
    words = collect_words_ending_with("g")
    for word in words:
        assert word[-1] == "g"
    words = collect_words_ending_with("ing")
    for word in words:
        assert word[-3:] == "ing"

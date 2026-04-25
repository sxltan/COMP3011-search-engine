from src.indexer import build_index, tokenize


def test_tokenize_lowercases_words():
    assert tokenize("Good GOOD good") == ["good", "good", "good"]


def test_tokenize_removes_punctuation():
    assert tokenize("Hello, world! This is good.") == [
        "hello",
        "world",
        "this",
        "is",
        "good",
    ]


def test_tokenize_handles_empty_text():
    assert tokenize("") == []


def test_build_index_tracks_frequency_and_positions():
    pages = [
        {"url": "page1", "text": "life is good life"},
        {"url": "page2", "text": "good friends"},
    ]

    index = build_index(pages)

    assert index["life"]["page1"]["frequency"] == 2
    assert index["life"]["page1"]["positions"] == [0, 3]
    assert index["good"]["page1"]["frequency"] == 1
    assert index["good"]["page2"]["frequency"] == 1


def test_build_index_is_case_insensitive():
    pages = [{"url": "page1", "text": "Good good GOOD"}]

    index = build_index(pages)

    assert index["good"]["page1"]["frequency"] == 3
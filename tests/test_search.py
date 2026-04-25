import pytest

from src.search import load_index, save_index


def test_save_and_load_index(tmp_path):
    index = {
        "life": {
            "page1": {
                "frequency": 2,
                "positions": [0, 3],
            }
        }
    }

    file_path = tmp_path / "index.json"

    save_index(index, file_path)
    loaded_index = load_index(file_path)

    assert loaded_index == index


def test_load_missing_index_raises_error(tmp_path):
    missing_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        load_index(missing_file)


def test_save_index_creates_parent_directory(tmp_path):
    index = {"word": {"page1": {"frequency": 1, "positions": [0]}}}
    file_path = tmp_path / "nested" / "index.json"

    save_index(index, file_path)

    assert file_path.exists()
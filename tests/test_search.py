import pytest

from src.main import find_pages, print_help, print_word, run_shell
from src.search import load_index, save_index


def sample_index():
    return {
        "good": {
            "page1": {"frequency": 2, "positions": [0, 3]},
            "page2": {"frequency": 1, "positions": [1]},
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [2]},
        },
    }


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


def test_print_help_outputs_commands(capsys):
    print_help()

    captured = capsys.readouterr()

    assert "build" in captured.out
    assert "load" in captured.out
    assert "find" in captured.out


def test_print_word_outputs_data(capsys):
    index = sample_index()

    print_word(index, "good")

    captured = capsys.readouterr()

    assert "page1" in captured.out
    assert "frequency" in captured.out


def test_print_word_handles_missing_word(capsys):
    index = sample_index()

    print_word(index, "unknown")

    captured = capsys.readouterr()

    assert "No results found" in captured.out


def test_find_pages_single_word(capsys):
    index = sample_index()

    find_pages(index, "good")

    captured = capsys.readouterr()

    assert "page1" in captured.out
    assert "page2" in captured.out


def test_find_pages_multi_word_intersection(capsys):
    index = sample_index()

    find_pages(index, "good friends")

    captured = capsys.readouterr()

    assert "page1" in captured.out
    assert "page2" not in captured.out


def test_find_pages_missing_term(capsys):
    index = sample_index()

    find_pages(index, "good unknown")

    captured = capsys.readouterr()

    assert "Missing term" in captured.out


def test_find_pages_empty_query(capsys):
    index = sample_index()

    find_pages(index, "")

    captured = capsys.readouterr()

    assert "Please provide at least one search term" in captured.out


def test_find_pages_ranks_results(capsys):
    index = sample_index()

    find_pages(index, "good")

    captured = capsys.readouterr()
    output = captured.out

    assert output.index("page1") < output.index("page2")


def test_run_shell_exits_cleanly(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "exit")

    run_shell()

    captured = capsys.readouterr()

    assert "Goodbye" in captured.out


def test_run_shell_handles_unknown_command(monkeypatch, capsys):
    commands = iter(["unknown", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    run_shell()

    captured = capsys.readouterr()

    assert "Unknown command" in captured.out


def test_run_shell_print_requires_loaded_index(monkeypatch, capsys):
    commands = iter(["print life", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(commands))

    run_shell()

    captured = capsys.readouterr()

    assert "No index loaded" in captured.out
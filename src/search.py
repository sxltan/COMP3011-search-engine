import json
from pathlib import Path


DEFAULT_INDEX_PATH = Path("data/index.json")


def save_index(index: dict, file_path: Path = DEFAULT_INDEX_PATH) -> None:
    """Save the inverted index to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(index, file, indent=2, ensure_ascii=False)


def load_index(file_path: Path = DEFAULT_INDEX_PATH) -> dict:
    """Load the inverted index from a JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"No index file found at {file_path}. Run 'build' before 'load'."
        )

    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)
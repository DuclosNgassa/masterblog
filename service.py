import json
from typing import Any


def read_json(path: str) -> list[dict]:
    data = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file '{path}' was not found.")
    except json.decoder.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from '{path}': {e}")

    return data


def write_json(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        )

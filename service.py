import json
from typing import Any, Optional


def read_json(path: str) -> list[dict]:
    """
    Reads a JSON file and returns a list of dictionaries.
    :param path: the file path
    :return: the list of dictionaries
    """
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
    """
    Writes a list of dictionaries to a JSON file.
    :param path: the file path
    :param data: the list of dictionaries to write
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            sort_keys=True,
            indent=4,
        )

def fetch_post_by_id(
    post_id: int, posts: list[dict[str, Any]]
) -> Optional[dict[str, Any]]:
    """Searches a list of post dictionaries for a post matching the given post_id.

    Returns the dictionary if found, or None if no match exists.
    """
    print(f"Fetching post with id: {post_id}")
    print(posts)
    for post in posts:
        if str(post.get("id")) == str(post_id):
            print(f"Found post with id: {post_id}")
            return post
    return None
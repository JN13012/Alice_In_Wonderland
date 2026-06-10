import json
from pathlib import Path

CACHE_DIR = Path("data/cache")


def get_cache_path(book_id, task_name):
    return CACHE_DIR / f"{book_id}_{task_name}.json"


def load_cache(book_id, task_name):
    path = get_cache_path(book_id, task_name)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf8") as file:
        return json.load(file)


def save_cache(book_id, task_name, data):
    path = get_cache_path(book_id, task_name)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

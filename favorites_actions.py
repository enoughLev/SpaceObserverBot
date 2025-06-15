import json
import os
from typing import List, Dict


def add_to_favorites(user_id: int, item: dict):
    filename = f'{user_id}_favorites.json'
    favorites = []

    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                favorites = json.load(f)
                if not isinstance(favorites, list):
                    favorites = []
        except (json.JSONDecodeError, FileNotFoundError):
            favorites = []

    favorites.append(item)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)


def get_favorites(user_id: int) -> List[Dict]:
    filename = f'{user_id}_favorites.json'
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            favorites = json.load(f)
            if isinstance(favorites, list):
                return favorites
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_favorites(user_id: int, favorites: List[Dict]):
    filename = f'{user_id}_favorites.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)

def delete_favorite_by_index(user_id: int, index: int) -> bool:
    favorites = get_favorites(user_id)
    if 0 <= index < len(favorites):
        favorites.pop(index)
        save_favorites(user_id, favorites)
        return True
    return False

def delete_all_favorites(user_id: int):
    favorites = get_favorites(user_id)
    while favorites:
        delete_favorite_by_index(user_id, 0)
        favorites = get_favorites(user_id)
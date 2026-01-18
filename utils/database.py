"""
Baddie's Bakery - Base de Données
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import uuid

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "posts.json")


def _ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _load_data() -> List[Dict]:
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_data(data: List[Dict]):
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_post(content: str, post_type: str, platform: str, 
              metadata: Optional[Dict] = None) -> str:
    posts = _load_data()
    post_id = str(uuid.uuid4())[:8]
    new_post = {
        "id": post_id,
        "content": content,
        "post_type": post_type,
        "platform": platform,
        "created_at": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    posts.insert(0, new_post)
    _save_data(posts)
    return post_id


def get_all_posts() -> List[Dict]:
    return _load_data()


def get_posts_by_type(post_type: str) -> List[Dict]:
    posts = _load_data()
    return [p for p in posts if p.get("post_type") == post_type]


def get_posts_by_platform(platform: str) -> List[Dict]:
    posts = _load_data()
    return [p for p in posts if p.get("platform") == platform]


def get_post_by_id(post_id: str) -> Optional[Dict]:
    posts = _load_data()
    for post in posts:
        if post.get("id") == post_id:
            return post
    return None


def delete_post(post_id: str) -> bool:
    posts = _load_data()
    for i, post in enumerate(posts):
        if post.get("id") == post_id:
            posts.pop(i)
            _save_data(posts)
            return True
    return False


def get_stats() -> Dict:
    posts = _load_data()
    types_count = {}
    for post in posts:
        post_type = post.get("post_type", "inconnu")
        types_count[post_type] = types_count.get(post_type, 0) + 1
    platforms_count = {}
    for post in posts:
        platform = post.get("platform", "inconnue")
        platforms_count[platform] = platforms_count.get(platform, 0) + 1
    return {
        "total": len(posts),
        "by_type": types_count,
        "by_platform": platforms_count
    }

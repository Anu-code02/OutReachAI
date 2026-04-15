import json
from typing import List, Dict, Any


import os

class FewShotPosts:
    def __init__(self, file_path: str = None):
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "data", "processed_posts.json")
        self.posts: List[Dict[str, Any]] = []
        self.unique_tags: List[str] = []
        self.load_posts(file_path)

    def load_posts(self, file_path: str):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            # compute derived fields
            for p in posts:
                p['length'] = self.categorize_length(p.get('line_count', 0))
            self.posts = posts
            # collect unique tags
            all_tags: List[str] = []
            for p in posts:
                tags = p.get('tags', []) or []
                all_tags.extend(tags)
            self.unique_tags = sorted(list(set(all_tags)))

    def get_filtered_posts(self, length: str, language: str, tag: str) -> List[Dict[str, Any]]:
        filtered: List[Dict[str, Any]] = []
        for p in self.posts:
            tags = p.get('tags', []) or []
            if tag in tags and p.get('language') == language and p.get('length') == length:
                filtered.append(p)
        return filtered

    def categorize_length(self, line_count: int) -> str:
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self) -> List[str]:
        return self.unique_tags


if __name__ == "__main__":
    fs = FewShotPosts()
    posts = fs.get_filtered_posts("Medium", "Hinglish", "Job Search")
    print(posts)
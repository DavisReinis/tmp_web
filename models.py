# models.py

import os
import json

class Entry:
    def __init__(self, entry_id, theater, title, date, tags, notes=""):
        self.id = entry_id
        self.theater = theater
        self.title = title
        self.date = date
        self.tags = tags
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "theater": self.theater,
            "title": self.title,
            "date": self.date,
            "tags": self.tags,
            "notes": self.notes
        }

class Data:
    def __init__(self, base_dir="data", entries_file="entries.json", tags_file="tags.json"):
        self.entries_path = os.path.join(base_dir, entries_file)
        self.tags_path = os.path.join(base_dir, tags_file)

    def load_entries(self):
        return self._load_json(self.entries_path)

    def load_tags(self):
        return self._load_json(self.tags_path)

    def save_entries(self, entries):
        self._save_json(entries, self.entries_path)

    def save_tags(self, tags):
        self._save_json(tags, self.tags_path)

    def _load_json(self, path):
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, data, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

#     def get_tag(self, id):
#         tags = self.load_tags()
#         for tag in tags:
#             if tag["id"] == id:
#                 return tag
#         return None


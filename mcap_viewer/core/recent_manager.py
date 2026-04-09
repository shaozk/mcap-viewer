import json
import os


class RecentFilesManager:
    def __init__(self, max_recent=5, config_file="recent_files.json"):
        self.max_recent = max_recent
        self.config_file = config_file
        self.recent_files = []
        self.load()

    def load(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.recent_files = data.get("recent_files", [])[: self.max_recent]
            except Exception as e:
                print(f"recent file error: {e}")
                self.recent_files = []

    def save(self):
        with open(self.config_file, "w") as f:
            json.dump({"recent_files": self.recent_files}, f)

    def add_file(self, filepath):
        if filepath in self.recent_files:
            self.recent_files.remove(filepath)
        self.recent_files.insert(0, filepath)
        # 保持最大数量限制
        self.recent_files = self.recent_files[: self.max_recent]
        self.save()

    def get(self):
        return self.recent_files.copy()

    def clear(self):
        self.recent_files = []
        self.save()

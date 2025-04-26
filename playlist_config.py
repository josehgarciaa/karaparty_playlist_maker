import yaml

class PlaylistConfig:
    def __init__(self, path):
        self.path = path
        self.data = self.load_config()

    def load_config(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_theme(self):
        return self.data.get('theme', '')

    def get_blocks(self):
        return self.data.get('blocks', [])

    def get_rules(self):
        return self.data.get('rules', {}) 
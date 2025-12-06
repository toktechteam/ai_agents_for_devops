class Memory:
    def __init__(self):
        self.store = {}

    def remember(self, key, value):
        self.store[key] = value

    def get(self, key, default=None):
        return self.store.get(key, default)

    def dump(self):
        return dict(self.store)

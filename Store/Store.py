class Store:
    def __init__(self, config) -> None:
        self.config = config


    def updateConfig(self, key, value, root='variables'):
        temp = self.config.get(root, {})
        temp[key] = value.decode().strip() if isinstance(value, bytes) else value
        self.config[root] = temp
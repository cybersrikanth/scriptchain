import json
from sys import argv
from Store.Store import Store

ConfigStore = None
prefix = argv[1] or ''
prefix = f'{prefix}.' if len(prefix) else prefix
with open(f'{prefix}config.json', 'r') as file:
    ConfigStore = Store(json.loads(file.read()))
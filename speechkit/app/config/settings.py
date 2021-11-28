from pathlib import Path

import yaml


BASE_DIR = Path(__file__).resolve().parent.parent

def read_config():
    with open(BASE_DIR / 'config' / 'config.yml', 'r') as ymlfile:
        data = yaml.safe_load(ymlfile)
    return data

config = read_config()

YANDEX_API_KEY = config['YANDEX_API_KEY']

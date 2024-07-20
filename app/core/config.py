import os
from . import logger

CONFIG_FILE = 'config.cfg'


def load_config():
    if os.path.exists(CONFIG_FILE):
        config = {}
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('//'):
                    key, value = line.split(' ', 1)
                    config[key] = value.strip().strip('"')
        return config
    return None


def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        for key, value in config.items():
            f.write(f'{key} "{value}"\n')


def prompt_for_csgo_dir():
    csgo_dir = input("未检测到CSGO程序，请启动CSGO后再加载本程序\n或手动输入CSGO路径: ")
    config = {
        "csgo_dir": csgo_dir
    }
    save_config(config)
    return config

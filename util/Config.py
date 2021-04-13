from os import remove
from os.path import isfile

from yaml import load as yaml_load

from util.CONSTANTS import CONFIG_FILE


def load_config():
    with open(CONFIG_FILE, 'r') as conf_file:
        data = yaml_load(conf_file)

    return data


def save_config(cookie1, cookie2):
    return 0


def delete_config():
    if isfile(CONFIG_FILE):
        remove(CONFIG_FILE)

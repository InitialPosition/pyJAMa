from os import remove
from os.path import isfile

from yaml import load as yaml_load, dump as yaml_dump, FullLoader

from util.CONSTANTS import CONFIG_FILE


def load_config():
    # make sure the config file exists
    if isfile(CONFIG_FILE) is False:
        print('Tried to load config but none present! Aborting...')
        exit(0)

    # read yaml from config file
    with open(CONFIG_FILE, 'r', encoding='utf8') as conf_file:
        data = yaml_load(conf_file, Loader=FullLoader)

    return data


def save_config(cookie1):
    # delete old config
    delete_config()

    # generate new yaml object
    yaml_object = {}

    # write cookies to yaml dict
    yaml_object.update({'SIDS': cookie1})

    # save cookies in config file
    with open(CONFIG_FILE, 'w', encoding='utf8') as conf_file:
        yaml_dump(yaml_object, conf_file)


def delete_config():
    if isfile(CONFIG_FILE):
        remove(CONFIG_FILE)

from enum import Enum
from os import remove
from os.path import isfile

from yaml import load as yaml_load, dump as yaml_dump, FullLoader

from util.CONSTANTS import CONFIG_FILE


class ConfigKeys(Enum):
	DARK_MODE = "DarkMode"


def load_config():
	# make sure the config file exists
	if isfile(CONFIG_FILE) is False:
		print('Tried to load config but none present! Aborting...')
		return None

	# read yaml from config file
	with open(CONFIG_FILE, 'r', encoding='utf8') as conf_file:
		data = yaml_load(conf_file, Loader=FullLoader)

	return data


def load_config_key(key: str):
	data = load_config()
	if data is not None:
		if key in data:
			return data[key]
		else:
			return None

	return None


def save_config(cookie1):
	# get current dark mode setting so we dont overwrite it
	dark_mode_enabled = load_config_key(ConfigKeys.DARK_MODE.value)
	# if we're coming from an older version without a dark mode value in the config, default to True
	if dark_mode_enabled is None:
		dark_mode_enabled = True

	# delete old config
	delete_config()

	# generate new yaml object
	yaml_object = {}

	# write data to yaml dict
	yaml_object.update({
		'SIDS': cookie1,
		ConfigKeys.DARK_MODE.value: dark_mode_enabled
	})

	# save cookies in config file
	with open(CONFIG_FILE, 'w', encoding='utf8') as conf_file:
		yaml_dump(yaml_object, conf_file)


def delete_config():
	if isfile(CONFIG_FILE):
		remove(CONFIG_FILE)


def has_config():
	return isfile(CONFIG_FILE)

import configparser
import platform
import sqlite3
from getpass import getuser
from os import path, getenv
from os.path import isdir
from sqlite3 import Error, OperationalError


def get_cookie_firefox():
    print('Attempting to fetch Firefox Cookie...')

    # get cookie database directory
    os = platform.system()
    appdata_dir = ''

    if os == 'Windows':
        appdata_dir = path.join(getenv('APPDATA'), 'Mozilla/Firefox')
    elif os == 'Linux':
        appdata_dir = path.join('/home/', getuser(), '.mozilla/firefox')
    else:
        print('Could not establish OS! Aborting cookie retrieval...')
        return -1

    if isdir(appdata_dir) is False:
        print('Firefox was not found on this system')
        return -1

    config_path = path.join(appdata_dir, 'profiles.ini')

    config = configparser.ConfigParser()
    config.read(config_path)
    database_path = path.join(appdata_dir, config['Profile0']['Path'], 'cookies.sqlite')

    # connect to cookie database and read cookie
    try:
        con = sqlite3.connect(database_path)
        cursor = con.cursor()

        cursor.execute('SELECT value FROM moz_cookies WHERE host=".ldjam.com" AND name="SIDS"')
        result = cursor.fetchone()
        token_raw = result[0]

        return token_raw

    except OperationalError:
        print('Could not fetch cookie, database was locked. Make sure Firefox is not running and try again!')
        exit()
    except Error:
        print('Unknown error while fetching Firefox Cookie.')
        return -1

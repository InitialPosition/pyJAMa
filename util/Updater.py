from enum import Enum
from os import remove
from zipfile import ZipFile

from requests import get, ConnectionError

from util.CONSTANTS import VERSION


class UpdateCheckResult(Enum):
    UPDATE_AVAILABLE = 0,
    NO_UPDATE_AVAILABLE = 1,
    CHECK_ERROR = 2


def check_for_update():
    # split local version into [major, minor, build] array
    local_version = VERSION.split('.')

    # fetch newest version from website
    try:
        version_request = get('https://raw.githubusercontent.com/InitialPosition/pyJAMa/main/util/CONSTANTS.py')

    except ConnectionError:
        print('Could not check for updates! Are you connected to the internet?')
        return UpdateCheckResult.CHECK_ERROR, None

    # stop here if request wasn't successful
    if version_request.status_code != 200:
        return UpdateCheckResult.CHECK_ERROR, None

    version_line = None
    for line in version_request.text.splitlines():
        if line.startswith('VERSION'):
            version_line = line
            break

    # if version line is still none, something went wrong
    if version_line is None:
        return UpdateCheckResult.CHECK_ERROR, None

    # extract newest version from version line
    online_version = version_line.split('\'')[1]
    online_version_split = online_version.split('.')

    # make version numbers
    local_final_version = ''
    online_final_version = ''
    for i in range(3):
        local_final_version += local_version[i]
        online_final_version += online_version_split[i]

    # compare versions and return proper status
    if int(online_final_version) > int(local_final_version):
        return UpdateCheckResult.UPDATE_AVAILABLE, online_version
    else:
        return UpdateCheckResult.NO_UPDATE_AVAILABLE, None


def download_update(new_version: str):
    update_zip_name = 'update.zip'

    # download update zip
    print(f'Downloading update...')
    download_url = f'https://github.com/InitialPosition/pyJAMa/releases/download/v{new_version}/pyJAMa.zip'
    download = get(download_url, stream=True)

    # save chunks to disk
    with open(update_zip_name, 'wb') as update_zip:
        for chunk in download.iter_content(chunk_size=1024):
            if chunk:
                update_zip.write(chunk)

    print('Unzipping...')
    # extract data and overwrite local files
    with ZipFile(update_zip_name) as final_zip:
        final_zip.extractall()

    print('Cleaning up...')
    remove(update_zip_name)

    print('Update completed! Please restart the program to apply the changes.')

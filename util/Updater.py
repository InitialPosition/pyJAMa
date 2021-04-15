from enum import Enum

from requests import get

from util.CONSTANTS import VERSION


class UpdateCheckResult(Enum):
    UPDATE_AVAILABLE = 0,
    NO_UPDATE_AVAILABLE = 1,
    CHECK_ERROR = 2


def check_for_update():
    # split local version into [major, minor, build] array
    local_version = VERSION.split('.')

    # fetch newest version from website
    version_request = get('https://raw.githubusercontent.com/InitialPosition/pyJAMa/main/util/CONSTANTS.py')

    # stop here if request wasn't successful
    if version_request.status_code != 200:
        return UpdateCheckResult.CHECK_ERROR

    version_line = None
    for line in version_request.text.splitlines():
        if line.startswith('VERSION'):
            version_line = line
            break

    # if version line is still none, something went wrong
    if version_line is None:
        return UpdateCheckResult.CHECK_ERROR

    # extract newest version from version line
    online_version = version_line.split('\'')[1].split('.')

    # make version numbers
    local_final_version = ''
    online_final_version = ''
    for i in range(3):
        local_final_version += local_version[i]
        online_final_version += online_version[i]

    # compare versions and return proper status
    if int(online_final_version) > int(local_final_version):
        return UpdateCheckResult.UPDATE_AVAILABLE
    else:
        return UpdateCheckResult.NO_UPDATE_AVAILABLE

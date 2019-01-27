from typing import Dict

from hestia.http import safe_request

from checks.base import Check
from checks.results import Result
from libs.api import get_settings_ws_api_url


class StreamsCheck(Check):

    @classmethod
    def run(cls) -> Dict:
        response = safe_request('{}/_health'.format(get_settings_ws_api_url()), 'GET')
        status_code = response.status_code
        if status_code == 200:
            result = Result()
        else:
            result = Result(message='Service is not healthy, response {}'.format(status_code),
                            severity=Result.ERROR)

        return {'STREAMS': result}

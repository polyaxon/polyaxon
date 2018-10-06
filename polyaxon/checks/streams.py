from checks.base import Check
from checks.results import Result
from libs.http import safe_request


class StreamsCheck(Check):

    @classmethod
    def run(cls):
        response = safe_request('', 'GET')
        status_code = response.status_code
        if status_code == 200:
            result = Result()
        else:
            result = Result(message='Service is not healthy, response {}'.format(status_code),
                            severity=Result.ERROR)

        return {'STREAMS': result}

from typing import Dict

from django.core.cache import CacheKeyWarning, cache

from checks.base import Check
from checks.results import Result


class CacheCheck(Check):

    @classmethod
    def run(cls) -> Dict:
        try:
            cache.set('health_check', 'test', 1)
            if cache.get('health_check') != 'test':
                result = Result(
                    message='Cache key does not match.',
                    severity=Result.ERROR
                )
            else:
                result = Result()
        except CacheKeyWarning:
            result = Result(
                message='Cache key warning.',
                severity=Result.ERROR
            )
        except ValueError:
            result = Result(
                message='Cache raised a ValueError.',
                severity=Result.ERROR
            )
        except ConnectionError:
            result = Result(
                message='Cache raised a ConnectionError.',
                severity=Result.ERROR
            )

        return {'CACHE': result}

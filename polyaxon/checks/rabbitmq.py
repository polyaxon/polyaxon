import logging

from typing import Dict

from amqp.exceptions import AccessRefused
from kombu import Connection

import conf

from checks.base import Check
from checks.results import Result

logger = logging.getLogger(__name__)


class RabbitMQCheck(Check):

    @staticmethod
    def check() -> Result:
        """Open and close the broker channel."""
        try:
            # Context to release connection
            with Connection(conf.get('CELERY_BROKER_URL')) as conn:
                conn.connect()
        except ConnectionRefusedError:
            return Result(message='Service unable to connect, "Connection was refused".',
                          severity=Result.ERROR)

        except AccessRefused:
            return Result(message='Service unable to connect, "Authentication error".',
                          severity=Result.ERROR)

        except IOError:
            return Result(message='Service has an "IOError".', severity=Result.ERROR)

        except Exception as e:
            return Result(message='Service has an "{}" error.'.format(e), severity=Result.ERROR)
        else:
            return Result()

    @classmethod
    def run(cls) -> Dict:
        return {'RABBITMQ': cls.check()}

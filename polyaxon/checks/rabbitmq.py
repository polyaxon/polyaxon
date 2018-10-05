import logging

from amqp.exceptions import AccessRefused
from kombu import Connection

from django.conf import settings

from checks.base import Check
from checks.results import Result

logger = logging.getLogger(__name__)


class RabbitMQCheck(Check):

    @staticmethod
    def check():
        """Open and close the broker channel."""
        try:
            # Context to release connection
            with Connection(settings.AMQP_URL) as conn:
                conn.connect()
        except ConnectionRefusedError:
            return Result(message='Service unable to connect, "Connection was refused".',
                          severity=Result.ERROR)

        except AccessRefused:
            Result(message='Service unable to connect, "Authentication error".',
                   severity=Result.ERROR)

        except IOError:
            return Result(message='Service has an "IOError".', severity=Result.ERROR)

        except Exception as e:
            return Result(message='Service has an "{}" error.'.format(e), severity=Result.ERROR)
        else:
            return Result()

    @classmethod
    def run(cls):
        return {'RABBITMQ': cls.check()}

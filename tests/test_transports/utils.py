from unittest import TestCase

from polyaxon_client import settings


class BaseTestCaseTransport(TestCase):
    def setUp(self):
        settings.MIN_TIMEOUT = 0.001

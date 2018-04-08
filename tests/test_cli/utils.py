# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from click.testing import CliRunner


class BaseCommandTestCase(TestCase):
    def setUp(self):
        self.runner = CliRunner()

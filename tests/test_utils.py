# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_stores.utils import is_protected_type, append_basename


class TestUtils(TestCase):
    def test_is_protected_type(self):
        assert is_protected_type(None) is True
        assert is_protected_type(1) is True
        assert is_protected_type(1.1) is True
        assert is_protected_type('foo') is False

    def test_append_basename(self):
        assert append_basename('foo', 'bar') == 'foo/bar'
        assert append_basename('foo', 'moo/bar') == 'foo/bar'
        assert append_basename('/foo', 'bar') == '/foo/bar'
        assert append_basename('/foo/moo', 'bar') == '/foo/moo/bar'
        assert append_basename('/foo/moo', 'boo/bar.txt') == '/foo/moo/bar.txt'


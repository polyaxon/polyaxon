# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tempfile

from unittest import TestCase

from polystores.utils import append_basename, get_files_in_current_directory, is_protected_type


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

    def test_get_files_in_current_directory(self):
        dirname = tempfile.mkdtemp()
        fpath1 = dirname + '/test1.txt'
        with open(fpath1, 'w') as f:
            f.write('data1')

        fpath2 = dirname + '/test2.txt'
        with open(fpath2, 'w') as f:
            f.write('data2')

        dirname2 = tempfile.mkdtemp(prefix=dirname + '/')
        fpath3 = dirname2 + '/test3.txt'
        with open(fpath3, 'w') as f:
            f.write('data3')

        with get_files_in_current_directory(dirname) as files:
            assert len(files) == 3
            assert set(files) == {fpath1, fpath2, fpath3}

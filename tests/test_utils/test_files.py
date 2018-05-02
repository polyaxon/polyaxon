# -*- coding: utf-8 -*-
import tarfile
from unittest import TestCase

import os

from polyaxon_cli.utils.files import create_tarfile


class TestFiles(TestCase):
    def test_create_tarfile(self):
        files = ['tests/test_utils/__init__.py']
        with create_tarfile(files, 'project_name') as tar_file_name:
            assert os.path.exists(tar_file_name)
            with tarfile.open(tar_file_name) as tf:
                members = tf.getmembers()
                assert set([m.name for m in members]) == set(files)
        assert not os.path.exists(tar_file_name)


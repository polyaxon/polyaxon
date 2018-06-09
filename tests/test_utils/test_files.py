# -*- coding: utf-8 -*-
import os
import tarfile

from unittest import TestCase

from polyaxon_cli.utils.files import create_tarfile, get_files_in_current_directory


class TestFiles(TestCase):
    def test_create_tarfile(self):
        files = ['tests/test_utils/__init__.py']
        with create_tarfile(files, 'project_name') as tar_file_name:
            assert os.path.exists(tar_file_name)
            with tarfile.open(tar_file_name) as tf:
                members = tf.getmembers()
                assert set([m.name for m in members]) == set(files)
        assert not os.path.exists(tar_file_name)

    def test_get_files_in_current_directory(self):
        file_paths = ['tests/test_utils/__init__.py']
        with get_files_in_current_directory('repo', file_paths) as (files, files_size):
            assert len(file_paths) == len(files)

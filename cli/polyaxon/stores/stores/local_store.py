# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import shutil

from polystores.logger import logger
from polystores.stores.base_store import BaseStore


class LocalStore(BaseStore):
    """
    Local filesystem store.

    This store is noop store since all data is accessible through the filesystem.
    """
    # pylint:disable=arguments-differ

    STORE_TYPE = BaseStore._LOCAL_STORE  # pylint:disable=protected-access

    @staticmethod
    def _list(path, check, abs_path=False):
        """
        List all entities directly under 'dir_name' that satisfy 'filter_func'

        Args:
            path: path where to start search
            check: function to check whether or not to include the results.
            abs_path: If True will return results with abs path.

        Returns:
            list of all files or directories under the path after the check.
        """
        if not os.path.isdir(path):
            raise Exception("Invalid parent directory '%s'" % path)
        matches = [x for x in os.listdir(path) if check(os.path.join(path, x))]
        return [os.path.join(path, m) for m in matches] if abs_path else matches

    def ls(self, path):
        return self.list(path=path)

    def list(self, path, abs_path=False):

        def list_dirs():
            return self._list(path, os.path.isdir, abs_path)

        def list_files():
            matches = self._list(path, os.path.isfile, abs_path)
            if abs_path:
                return [(f, os.path.getsize(f)) for f in matches]
            return [(f, os.path.getsize(os.path.join(path, f))) for f in matches]

        return {
            'dirs': list_dirs(),
            'files': list_files()
        }

    def download_file(self, *args, **kwargs):
        pass

    def upload_file(self, *args, **kwargs):
        pass

    def upload_dir(self, *args, **kwargs):
        pass

    def download_dir(self, *args, **kwargs):
        pass

    def delete(self, path, **kwargs):
        if not os.path.exists(path):
            return
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except OSError:
            logger.warning('Could not delete path `%s`', path)

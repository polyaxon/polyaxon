import logging
import os
import shutil

_logger = logging.getLogger('polyaxon.libs.paths')


def delete_path(path):
    if not os.path.exists(path):
        return
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except OSError:
        _logger.warning('Could not delete path `%s`', path)


def create_path(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except OSError as e:
        _logger.warning('Could not create path `%s`, exception %s', path, e)


def get_tmp_path(path):
    return os.path.join('/tmp', path)


def create_tmp_dir(dir_name):
    create_path(get_tmp_path(dir_name))


def delete_tmp_dir(dir_name):
    delete_path(get_tmp_path(dir_name))


def copy_to_tmp_dir(path, dir_name):
    tmp_path = get_tmp_path(dir_name)
    if os.path.exists(tmp_path):
        return tmp_path
    try:
        shutil.copytree(path, tmp_path)
    except FileExistsError as e:
        _logger.warning('Path already exists `%s`, exception %s', path, e)
    return tmp_path

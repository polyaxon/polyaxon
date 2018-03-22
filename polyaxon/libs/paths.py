import logging
import os
import shutil

logger = logging.getLogger('polyaxon.libs.paths')


def delete_path(path):
    if not os.path.exists(path):
        return
    try:
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    except OSError:
        logger.warning('Could not delete path `{}`'.format(path))


def create_path(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.warning('Could not create path `{}`, exception %s', e)


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
    shutil.copytree(path, tmp_path)
    return tmp_path

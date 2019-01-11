import os
import tarfile

from polystores.exceptions import PolyaxonStoresException
from rest_framework.exceptions import ValidationError

import conf
import stores

from libs.paths.utils import check_archive_path
from stores.exceptions import VolumeNotFoundError


def create_tarfile(files, tar_path):
    """Create a tar file based on the list of files passed"""
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in files:
            tar.add(f)


def get_files_in_path(path):
    result_files = []
    for root, _, files in os.walk(path):
        for file_name in files:
            result_files.append(os.path.join(root, file_name))
    return result_files


def archive_repo(repo_git, repo_name, commit=None):
    archive_root = conf.get('REPOS_ARCHIVE_ROOT')
    check_archive_path(archive_root)
    archive_name = '{}-{}.tar.gz'.format(repo_name, commit or 'master')
    with open(os.path.join(archive_root, archive_name), 'wb') as fp:
        repo_git.archive(fp, format='tgz', treeish=commit)

    return archive_root, archive_name


def archive_outputs(outputs_path, name):
    archive_root = conf.get('OUTPUTS_ARCHIVE_ROOT')
    check_archive_path(archive_root)
    outputs_files = get_files_in_path(outputs_path)
    tar_name = "{}.tar.gz".format(name.replace('.', '_'))
    create_tarfile(files=outputs_files, tar_path=os.path.join(archive_root, tar_name))
    return archive_root, tar_name


def archive_outputs_file(outputs_path, namepath, filepath, persistence_outputs):
    check_archive_path(conf.get('OUTPUTS_DOWNLOAD_ROOT'))
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(conf.get('OUTPUTS_DOWNLOAD_ROOT'), namepath, filepath)
    download_dir = '/'.join(download_filepath.split('/')[:-1])
    check_archive_path(download_dir)
    try:
        store_manager = stores.get_outputs_store(persistence_outputs=persistence_outputs)
    except (PolyaxonStoresException, VolumeNotFoundError) as e:
        raise ValidationError(e)
    outputs_filepath = os.path.join(outputs_path, filepath)
    store_manager.download_file(outputs_filepath, download_filepath)
    if store_manager.store.is_local_store:
        return outputs_filepath
    return download_filepath


def archive_logs_file(log_path, namepath, persistence_logs='default'):
    check_archive_path(conf.get('LOGS_DOWNLOAD_ROOT'))
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(conf.get('LOGS_DOWNLOAD_ROOT'), namepath)
    download_dir = '/'.join(download_filepath.split('/')[:-1])
    check_archive_path(download_dir)
    try:
        store_manager = stores.get_logs_store(persistence_logs=persistence_logs)
    except (PolyaxonStoresException, VolumeNotFoundError) as e:
        raise ValidationError(e)
    store_manager.download_file(log_path, download_filepath)
    if store_manager.store.is_local_store:
        return log_path
    return download_filepath

import os
import tarfile

from typing import Any, List, Tuple

from hestia.paths import check_or_create_path
from polystores.exceptions import PolyaxonStoresException
from rest_framework.exceptions import ValidationError

import conf
import stores

from stores.exceptions import VolumeNotFoundError  # pylint:disable=ungrouped-imports


def create_tarfile(files: List[str], tar_path: str) -> None:
    """Create a tar file based on the list of files passed"""
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in files:
            tar.add(f)


def get_files_in_path(path: str) -> List[str]:
    result_files = []
    for root, _, files in os.walk(path):
        for file_name in files:
            result_files.append(os.path.join(root, file_name))
    return result_files


def archive_repo(repo_git: Any, repo_name: str, commit: str = None) -> Tuple[str, str]:
    archive_root = conf.get('REPOS_ARCHIVE_ROOT')
    check_or_create_path(archive_root)
    archive_name = '{}-{}.tar.gz'.format(repo_name, commit or 'master')
    with open(os.path.join(archive_root, archive_name), 'wb') as fp:
        repo_git.archive(fp, format='tgz', treeish=commit)

    return archive_root, archive_name


def archive_outputs(outputs_path: str, name: str) -> Tuple[str, str]:
    archive_root = conf.get('OUTPUTS_ARCHIVE_ROOT')
    check_or_create_path(archive_root)
    outputs_files = get_files_in_path(outputs_path)
    tar_name = "{}.tar.gz".format(name.replace('.', '_'))
    create_tarfile(files=outputs_files, tar_path=os.path.join(archive_root, tar_name))
    return archive_root, tar_name


def archive_outputs_file(outputs_path: str,
                         namepath: str,
                         filepath: str,
                         persistence_outputs: str) -> str:
    check_or_create_path(conf.get('OUTPUTS_DOWNLOAD_ROOT'))
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(conf.get('OUTPUTS_DOWNLOAD_ROOT'), namepath, filepath)
    download_dir = '/'.join(download_filepath.split('/')[:-1])
    check_or_create_path(download_dir)
    try:
        store_manager = stores.get_outputs_store(persistence_outputs=persistence_outputs)
        outputs_filepath = os.path.join(outputs_path, filepath)
        store_manager.download_file(outputs_filepath, download_filepath)
    except (PolyaxonStoresException, VolumeNotFoundError) as e:
        raise ValidationError(e)
    if store_manager.store.is_local_store:
        return outputs_filepath
    return download_filepath


def archive_logs_file(log_path: str, namepath: str, persistence_logs: str = 'default') -> str:
    check_or_create_path(conf.get('LOGS_DOWNLOAD_ROOT'))
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(conf.get('LOGS_DOWNLOAD_ROOT'), namepath)
    download_dir = '/'.join(download_filepath.split('/')[:-1])
    check_or_create_path(download_dir)
    try:
        store_manager = stores.get_logs_store(persistence_logs=persistence_logs)
        store_manager.download_file(log_path, download_filepath)
    except (PolyaxonStoresException, VolumeNotFoundError) as e:
        raise ValidationError(e)
    if store_manager.store.is_local_store:
        return log_path
    return download_filepath

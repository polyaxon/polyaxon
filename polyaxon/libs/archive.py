import os
import tarfile

from typing import Any, List, Tuple

from hestia.paths import check_or_create_path
from polystores.exceptions import PolyaxonStoresException
from rest_framework.exceptions import ValidationError

import conf
import stores

from options.registry.archives import ARCHIVES_ROOT_ARTIFACTS, ARCHIVES_ROOT_REPOS
from options.registry.downloads import DOWNLOADS_ROOT_ARTIFACTS, DOWNLOADS_ROOT_LOGS
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
    archive_root = conf.get(ARCHIVES_ROOT_REPOS)
    check_or_create_path(archive_root)
    archive_name = '{}-{}.tar.gz'.format(repo_name, commit or 'master')
    with open(os.path.join(archive_root, archive_name), 'wb') as fp:
        repo_git.archive(fp, format='tgz', treeish=commit)

    return archive_root, archive_name


def archive_outputs(outputs_path: str, namepath: str, persistence_outputs: str) -> Tuple[str, str]:
    archive_root = conf.get(ARCHIVES_ROOT_ARTIFACTS)
    check_or_create_path(archive_root)

    check_or_create_path(conf.get(DOWNLOADS_ROOT_ARTIFACTS))
    download_path = os.path.join(conf.get(DOWNLOADS_ROOT_ARTIFACTS), namepath.replace('.', '/'))
    download_dir = '/'.join(download_path.split('/'))
    check_or_create_path(download_dir)

    try:
        store_manager = stores.get_outputs_store(persistence_outputs=persistence_outputs)
        store_manager.download_dir(outputs_path, download_path)
    except (PolyaxonStoresException, VolumeNotFoundError) as e:
        raise ValidationError(e)

    if store_manager.store.is_local_store:
        outputs_files = get_files_in_path(outputs_path)
    else:
        outputs_files = get_files_in_path(download_path)
    tar_name = "{}.tar.gz".format(namepath.replace('.', '_'))
    create_tarfile(files=outputs_files, tar_path=os.path.join(archive_root, tar_name))
    return archive_root, tar_name


def archive_outputs_file(outputs_path: str,
                         namepath: str,
                         filepath: str,
                         persistence_outputs: str) -> str:
    check_or_create_path(conf.get(DOWNLOADS_ROOT_ARTIFACTS))
    download_filepath = os.path.join(conf.get(DOWNLOADS_ROOT_ARTIFACTS),
                                     namepath.replace('.', '/'),
                                     filepath)
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
    check_or_create_path(conf.get(DOWNLOADS_ROOT_LOGS))
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(conf.get(DOWNLOADS_ROOT_LOGS), namepath)
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

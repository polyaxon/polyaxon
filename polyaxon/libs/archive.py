import os
import tarfile

from django.conf import settings

import stores

from libs.paths.utils import check_archive_path


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
    check_archive_path(settings.REPOS_ARCHIVE_ROOT)
    archive_name = '{}-{}.tar.gz'.format(repo_name, commit or 'master')
    with open(os.path.join(settings.REPOS_ARCHIVE_ROOT, archive_name), 'wb') as fp:
        repo_git.archive(fp, format='tgz', treeish=commit)

    return settings.REPOS_ARCHIVE_ROOT, archive_name


def archive_outputs(outputs_path, name):
    check_archive_path(settings.OUTPUTS_ARCHIVE_ROOT)
    outputs_files = get_files_in_path(outputs_path)
    tar_name = "{}.tar.gz".format(name.replace('.', '_'))
    create_tarfile(files=outputs_files, tar_path=os.path.join(settings.OUTPUTS_ARCHIVE_ROOT,
                                                              tar_name))
    return settings.OUTPUTS_ARCHIVE_ROOT, tar_name


def archive_outputs_file(persistence_outputs, outputs_path, namepath, filepath):
    check_archive_path(settings.OUTPUTS_DOWNLOAD_ROOT)
    namepath = namepath.replace('.', '/')
    download_filepath = os.path.join(settings.OUTPUTS_DOWNLOAD_ROOT, namepath, filepath)
    download_dir = '/'.join(download_filepath.split('/')[:-1])
    check_archive_path(download_dir)
    store_manager = stores.get_outputs_store(persistence_outputs=persistence_outputs)
    outputs_filepath = os.path.join(outputs_path, filepath)
    store_manager.download_file(outputs_filepath, download_filepath)
    if store_manager.store.is_local_store:
        return outputs_filepath
    return download_filepath

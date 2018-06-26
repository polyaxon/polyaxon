import os
import tarfile

from django.conf import settings

from libs.paths.experiments import get_experiment_outputs_path


def check_archive_path(archive_path=None):
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)


def create_tarfile(files, tar_path):
    """Create a tar file based on the list of files passed"""
    with tarfile.open(tar_path, "w:gz") as tar:
        for f in files:
            tar.add(f)


def get_files_in_path(path):
    result_files = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            result_files.append(os.path.join(root, file_name))
    return result_files


def archive_repo(repo_git, repo_name):
    check_archive_path(settings.REPOS_ARCHIVE_ROOT)
    archive_name = '{}.tar.gz'.format(repo_name)
    with open(os.path.join(settings.REPOS_ARCHIVE_ROOT, archive_name), 'wb') as fp:
        repo_git.archive(fp, format='tgz')

    return settings.REPOS_ARCHIVE_ROOT, archive_name


def archive_experiment_outputs(experiment_name):
    check_archive_path(settings.OUTPUTS_ARCHIVE_ROOT)
    experiment_outputs_path = get_experiment_outputs_path(experiment_name)
    outputs_files = get_files_in_path(experiment_outputs_path)
    tar_name = "{}.tar.gz".format(experiment_name.replace('.', '_'))
    create_tarfile(files=outputs_files, tar_path=os.path.join(settings.OUTPUTS_ARCHIVE_ROOT,
                                                              tar_name))
    return settings.OUTPUTS_ARCHIVE_ROOT, tar_name

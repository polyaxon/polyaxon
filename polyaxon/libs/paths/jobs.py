import os

from hestia.paths import create_path


def get_job_subpath(job_name: str) -> str:
    return job_name.replace('.', '/')


def create_job_path(job_name: str, path: str) -> str:
    values = job_name.split('.')

    for value in values[:-1]:
        path = os.path.join(path, value)
        if not os.path.isdir(path):
            create_path(path)

    return path

import os

from libs.paths.outputs_paths import get_outputs_paths


def get_notebook_job_outputs_path(persistence_outputs, notebook_job):
    persistence_outputs = get_outputs_paths(persistence_outputs)
    return os.path.join(persistence_outputs, notebook_job.replace('.', '/'))

import fcntl

from polyaxon_schemas.utils import to_list

from libs.paths.experiments import create_experiment_logs_path, get_experiment_logs_path
from libs.paths.jobs import create_job_logs_path, get_job_logs_path


def _lock_log(log_path, log_lines):
    log_lines = to_list(log_lines)
    with open(log_path, "a") as log_file:
        fcntl.flock(log_file, fcntl.LOCK_EX)
        log_file.write('\n'.join(log_lines) + '\n')
        fcntl.flock(log_file, fcntl.LOCK_UN)


def safe_log_job(job_name, log_lines):
    log_path = get_job_logs_path(job_name)
    try:
        _lock_log(log_path, log_lines)
    except (FileNotFoundError, OSError):
        create_job_logs_path(job_name=job_name)
        # Retry
        _lock_log(log_path, log_lines)


def safe_log_experiment_job(experiment_name, log_lines):
    log_path = get_experiment_logs_path(experiment_name)
    try:
        _lock_log(log_path, log_lines)
    except (FileNotFoundError, OSError):
        create_experiment_logs_path(experiment_name=experiment_name)
        # Retry
        _lock_log(log_path, log_lines)

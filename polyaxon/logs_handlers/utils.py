import fcntl

from libs.paths.experiment_jobs import create_experiment_job_logs_path, get_experiment_job_logs_path
from libs.paths.experiments import create_experiment_logs_path, get_experiment_logs_path
from libs.paths.jobs import create_job_logs_path, get_job_logs_path


def _lock_log(log_path, log_lines, append=False):
    write_mode = 'a' if append else 'w'
    with open(log_path, write_mode) as log_file:
        fcntl.flock(log_file, fcntl.LOCK_EX)
        log_file.write(log_lines + '\n')
        fcntl.flock(log_file, fcntl.LOCK_UN)


def safe_log_job(job_name, log_lines, temp, append=False):
    log_path = get_job_logs_path(job_name, temp)
    try:
        _lock_log(log_path, log_lines, append=append)
    except OSError:
        create_job_logs_path(job_name=job_name, temp=temp)
        # Retry
        _lock_log(log_path, log_lines, append=append)


def safe_log_experiment(experiment_name, log_lines, temp, append=False):
    log_path = get_experiment_logs_path(experiment_name, temp)
    try:
        _lock_log(log_path, log_lines, append=append)
    except OSError:
        create_experiment_logs_path(experiment_name=experiment_name, temp=temp)
        # Retry
        _lock_log(log_path, log_lines, append=append)


def safe_log_experiment_job(experiment_job_name, log_lines, temp, append=False):
    log_path = get_experiment_job_logs_path(experiment_job_name, temp)
    try:
        _lock_log(log_path, log_lines, append=append)
    except OSError:
        create_experiment_job_logs_path(experiment_job_name=experiment_job_name, temp=temp)
        # Retry
        _lock_log(log_path, log_lines, append=append)

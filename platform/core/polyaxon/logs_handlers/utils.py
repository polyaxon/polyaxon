import fcntl

from typing import Iterable, Optional, Union

import stores


def _lock_log(log_path: str,
              log_lines: Optional[Union[str, Iterable[str]]],
              append: bool = False) -> None:
    if not log_lines:
        return
    write_mode = 'a' if append else 'w'
    with open(log_path, write_mode) as log_file:
        fcntl.flock(log_file, fcntl.LOCK_EX)
        log_file.write(log_lines + '\n')
        fcntl.flock(log_file, fcntl.LOCK_UN)


def safe_log_job(job_name: str,
                 log_lines: Optional[Union[str, Iterable[str]]],
                 temp: bool,
                 append: bool = False) -> None:
    def _safe_log_job(_temp=temp):
        log_path = stores.get_job_logs_path(job_name=job_name, temp=_temp)
        try:
            stores.create_job_logs_path(job_name=job_name, temp=_temp)
            _lock_log(log_path, log_lines, append=append)
        except OSError:
            # Retry
            stores.create_job_logs_path(job_name=job_name, temp=_temp)
            _lock_log(log_path, log_lines, append=append)

    # We are storing a temp file or a mounted path
    if temp or not stores.is_bucket_logs_persistence():
        _safe_log_job()
    else:
        # We are storing a file to bucket; Store the file as temp and then upload it
        _safe_log_job(True)
        stores.upload_job_logs(job_name=job_name)  # Add to stores


def safe_log_experiment(experiment_name: str,
                        log_lines: Optional[Union[str, Iterable[str]]],
                        temp: bool,
                        append: bool = False) -> None:
    def _safe_log_experiment(_temp=temp):
        log_path = stores.get_experiment_logs_path(
            experiment_name=experiment_name,
            temp=_temp)
        try:
            stores.create_experiment_logs_path(experiment_name=experiment_name, temp=_temp)
            _lock_log(log_path, log_lines, append=append)
        except OSError:
            # Retry
            stores.create_experiment_logs_path(experiment_name=experiment_name, temp=_temp)
            _lock_log(log_path, log_lines, append=append)

    # Check if we are appending and the store is local
    if append and not stores.is_bucket_logs_persistence():
        _safe_log_experiment(False)
    elif temp or not stores.is_bucket_logs_persistence():
        # We are storing a temp file or a mounted path
        _safe_log_experiment()
    else:
        # We are storing a file to bucket; Store the file as temp and then upload it
        _safe_log_experiment(True)
        stores.upload_experiment_logs(experiment_name=experiment_name)


def safe_log_experiment_job(experiment_job_name: str,
                            log_lines: Optional[Union[str, Iterable[str]]],
                            temp: bool,
                            append: bool = False) -> None:
    def _safe_log_experiment_job(_temp=temp):
        log_path = stores.get_experiment_job_logs_path(experiment_job_name=experiment_job_name,
                                                       temp=_temp)
        try:
            stores.create_experiment_job_logs_path(experiment_job_name=experiment_job_name,
                                                   temp=_temp)
            _lock_log(log_path, log_lines, append=append)
        except OSError:
            # Retry
            stores.create_experiment_job_logs_path(experiment_job_name=experiment_job_name,
                                                   temp=_temp)
            _lock_log(log_path, log_lines, append=append)

    # We are storing a temp file or a mounted path
    if temp or not stores.is_bucket_logs_persistence():
        _safe_log_experiment_job()
    else:
        # We are storing a file to bucket; Store the file as temp and then upload it
        _safe_log_experiment_job(True)
        stores.upload_experiment_job_logs(experiment_job_name=experiment_job_name)

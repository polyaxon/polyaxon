# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import json

import os
import signal
import subprocess
import sys

import time

from six.moves import xrange

from multiprocessing import Process

from tensorflow.python.platform import tf_logging as logging

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.utils import TaskType

from polyaxon.polyaxonfile.manager import (
    prepare_all_experiment_jobs,
    start_experiment_run,
)

jobs = []
processes = []
current_run = {'finished': False, TaskType.MASTER: None}


def cleanup():
    for job in jobs:
        job.terminate()
        job.join()


# Register cleanup function to the exit of this module
atexit.register(cleanup)


def signal_handler(*args):
    for p in processes:
        p.terminate()

    current_run['finished'] = True


def check_master_process():
    print([p.is_alive() for p in jobs])
    if not current_run['master'].is_alive():
        signal_handler()
        cleanup()


def get_pybin():
    try:
        pybin = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/python')
    except:  # pylint: disable=bare-except
        pybin = sys.executable
    return pybin


def run_cmd(pybin, cmd, cwd):
    env_cmd = '{} {}'.format(pybin, cmd)
    signal.signal(signal.SIGINT, signal_handler)
    logging.info(env_cmd)
    p = subprocess.Popen(env_cmd, cwd=cwd, shell=True)
    processes.append(p)
    _, error = p.communicate()
    if error:
        logging.error('{} - ERROR: '.format(error))


def create_process(env):
    cmd = ("""-c \"from polyaxon.polyaxonfile.local_runner import start_experiment_run;
start_experiment_run(
    '{polyaxonfile}', '{experiment_id}', '{task_type}', {task_id}, '{schedule}')\"""".format(
        **env))
    p = Process(target=run_cmd, args=(get_pybin(), cmd, os.getcwd(),))
    p.daemon = True
    p.start()
    jobs.append(p)
    if env['task_type'] == TaskType.MASTER:
        current_run[TaskType.MASTER] = p


def run_experiment(spec_config, xp):
    spec = Specification.read(spec_config)
    logging.info("running Experiment n: {}".format(xp))
    cluster, is_distributed = spec.cluster_def
    if not is_distributed:
        start_experiment_run(spec, xp, TaskType.MASTER, 0, 'continuous_train_and_eval')
        current_run['finished'] = True
    else:
        env = {
            'polyaxonfile': json.dumps(spec.parsed_data),
            'task_type': TaskType.MASTER,
            'experiment_id': xp,
            'task_id': 0,
            'schedule': 'train_and_evaluate'
        }

        create_process(env)

        for i in xrange(cluster.get(TaskType.WORKER, 0)):
            env['task_id'] = i
            env['task_type'] = TaskType.WORKER
            env['schedule'] = 'train'
            create_process(env)

        for i in xrange(cluster.get(TaskType.PS, 0)):
            env['task_id'] = i
            env['task_type'] = TaskType.PS
            env['schedule'] = 'run_std_server'
            create_process(env)

        for job in jobs:
            job.join()


def run(polyaxonfile):
    plx_file = PolyaxonFile.read(polyaxonfile)
    for xp in range(plx_file.matrix_space):
        run_experiment(plx_file.experiment_specs[xp], xp)

        while not current_run['finished']:
            check_master_process()
            time.sleep(10)

        current_run['finished'] = False
        current_run['master'] = None


def run_all(polyaxonfile):
    plx_file = PolyaxonFile.read(polyaxonfile)
    for xp in range(plx_file.matrix_space):
        xp_jobs = prepare_all_experiment_jobs(plx_file.experiment_specs[xp], xp)
        for i, xp_job in enumerate(xp_jobs):
            if i == 0:
                schedule = 'train_and_evaluate'
            else:
                schedule = 'train'
            p = Process(target=getattr(xp_job, schedule))
            p.start()
            jobs.append(p)

        for job in jobs:
            job.join()

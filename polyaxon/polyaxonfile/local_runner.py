# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
import os
import signal
import subprocess
import sys

import time
from six.moves import xrange
from multiprocessing import Process

from tensorflow.python.platform import tf_logging as logging

from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile

from polyaxon.estimators.run_config import TaskType
from polyaxon.polyaxonfile.manager import (
    prepare_all_experiment_runs,
    prepare_experiment_run,
)

jobs = []
processes = []
current_run = {'finished': False}


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
    sys.exit(0)


def get_pybin():
    try:
        pybin = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/python')
    except:  # pylint: disable=bare-except
        pybin = sys.executable
    return pybin


def start_experiment_run(polyaxonfile, experiment_id, task_type, task_id, schedule):
    plx_file = PolyaxonFile.read(polyaxonfile)
    experiment = prepare_experiment_run(plx_file, experiment_id, task_type, task_id)
    task = getattr(experiment, schedule)
    return task()


def run_cmd(pybin, cmd, cwd):
    env_cmd = '{} {}'.format(pybin, cmd)
    signal.signal(signal.SIGINT, signal_handler)
    logging.info(env_cmd)
    p = subprocess.Popen(env_cmd, cwd=cwd, shell=True)
    processes.append(p)
    _, error = p.communicate()
    if error:
        logging.info('{} - ERROR: '.format(error))


def create_process(env):
    cmd = ("""-c \"from polyaxon.polyaxonfile.local_runner import run_experiment;
           run_experiment('{polyaxonfile}', '{task_type}', {task_id}, '{schedule}')\"""".format(
        **env))
    p = Process(target=run_cmd, args=(get_pybin(), cmd, os.getcwd(),))
    p.daemon = True
    p.start()
    jobs.append(p)


def run(polyaxonfile):
    plx_file = PolyaxonFile.read(polyaxonfile)
    for xp in range(plx_file.matrix_space):
        logging.info("running Experiment n: {}".format(xp))
        cluster, is_distributed = plx_file.get_cluster_def_at(xp)
        if not is_distributed:
            start_experiment_run(plx_file, xp, TaskType.MASTER, 0, 'continuous_train_and_eval')
            current_run['finished'] = True
        else:
            env = {
                'polyaxonfile': polyaxonfile,
                'task_type': TaskType.MASTER,
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

        while not current_run['finished']:
            time.sleep(30)

        current_run['finished'] = False


def run_all(polyaxonfile):
    plx_file = PolyaxonFile.read(polyaxonfile)
    for xp in range(plx_file.matrix_space):
        xp_runs = prepare_all_experiment_runs(polyaxonfile, xp)
        for i, xp_run in enumerate(xp_runs):
            if i == 0:
                schedule = 'train_and_evaluate'
            else:
                schedule = 'train'
            p = Process(target=getattr(xp_run, schedule))
            p.start()
            jobs.append(p)

        for job in jobs:
            job.join()

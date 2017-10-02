# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import atexit
from multiprocessing import Process


# List that stores all the children processes of this module
from polyaxon.polyaxonfile.manager import prepare_experiments

jobs = []


def cleanup():
    """ Kills all the children processes.
    """
    for job in jobs:
        job.terminate()
        job.join()


# Register cleanup function to the exit of this module
atexit.register(cleanup)


def run_experiment(experiment, schedule):
    task = getattr(experiment, schedule)
    return task()


def run(polyaxonfil):
    xps = prepare_experiments(polyaxonfil)
    for i, xp in enumerate(xps):
        if i == 0:
            schedule = 'continuous_train_and_eval'
        else:
            schedule = 'train'
        p = Process(target=run_experiment, args=(xp, schedule))
        p.start()
        jobs.append(p)

    for job in jobs:
        job.join()

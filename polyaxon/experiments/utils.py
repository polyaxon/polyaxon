# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from tensorflow.contrib.learn.python.learn.learn_runner import _is_distributed
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.python.platform import tf_logging as logging

from polyaxon.experiments.experiment import Experiment


def _get_default_schedule(config):
    """Returns the default schedule for the provided RunConfig."""
    if not config or not _is_distributed(config):
        return 'train_and_evaluate'

    if not config.task_type:
        raise ValueError("Must specify a schedule")

    if config.task_type == run_config.TaskType.MASTER:
        # TODO(rhaertel): handle the case where there is more than one master
        # or explicitly disallow such a case.
        return 'train_and_evaluate'
    elif config.task_type == run_config.TaskType.PS:
        return 'run_std_server'
    elif config.task_type == run_config.TaskType.WORKER:
        return 'train'

    raise ValueError("No default schedule for task type: {}".format(config.task_type))


def _execute_schedule(experiment, schedule):
    """Execute the method named `schedule` of `experiment`."""
    if not hasattr(experiment, schedule):
        logging.error("Schedule references non-existent task {}".format(schedule))
        valid_tasks = [x for x in dir(experiment)
                       if not x.startswith('_')
                       and callable(getattr(experiment, x))]
        logging.error("Allowed values for this experiment are: {}".format(valid_tasks))
        raise ValueError("Schedule references non-existent task {}".format(schedule))

    task = getattr(experiment, schedule)
    if not callable(task):
        logging.error("Schedule references non-callable member {}".format(schedule))
        valid_tasks = [x for x in dir(experiment)
                       if not x.startswith('_')
                       and callable(getattr(experiment, x))]
        logging.error("Allowed values for this experiment are: {}".format(valid_tasks))
        raise TypeError("Schedule references non-callable member {}".format(schedule))
    return task()


def run_experiment(experiment_fn, output_dir, schedule=None):
    """Make and run an experiment.

    It creates an Experiment by calling `experiment_fn`. Then it calls the
    function named as `schedule` of the Experiment.

    If schedule is not provided, then the default schedule for the current task
    type is used. The defaults are as follows:

    * 'ps' maps to 'serve'
    * 'worker' maps to 'train'
    * 'master' maps to 'local_run'

    If the experiment's config does not include a task type, then an exception
    is raised.

    Example:
    ```python
    >>> def _create_my_experiment(output_dir):
    >>>     return tf.contrib.learn.Experiment(
    >>>         estimator=my_estimator(model_dir=output_dir),
    >>>         train_input_fn=my_train_input,
    >>>         eval_input_fn=my_eval_input)

    >>> run(experiment_fn=_create_my_experiment,
    >>>     output_dir="some/output/dir",
    >>>     schedule="train")
    ```

    Args:
        experiment_fn: A function that creates an `Experiment`. It should accept an
          argument `output_dir` which should be used to create the `Estimator`
          (passed as `model_dir` to its constructor). It must return an
          `Experiment`.
        output_dir: Base output directory.
        schedule: The name of the  method in the `Experiment` to run.

    Returns:
        The return value of function `schedule`.

    Raises:
        ValueError: If `output_dir` is empty, `schedule` is None but no task
          type is set in the built experiment's config, the task type has no
          default, or `schedule` doesn't reference a member of `Experiment`.
        TypeError: `schedule` references non-callable member.
    """
    if not output_dir:
        raise ValueError("Must specify an output directory")
    if not callable(experiment_fn):
        raise TypeError("Experiment builder `{}` is not callable.".format(experiment_fn))

    # Call the builder
    experiment = experiment_fn(output_dir=output_dir)
    if not isinstance(experiment, Experiment):
        raise TypeError("Experiment builder did not return an Experiment instance, "
                        "got {} instead.".format(type(experiment)))

    # Get the schedule
    config = experiment.estimator.config
    schedule = schedule or _get_default_schedule(config)

    return _execute_schedule(experiment, schedule)

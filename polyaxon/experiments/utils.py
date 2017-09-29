# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.contrib.learn.python.learn import learn_runner


def run_experiment(experiment_fn, output_dir=None, schedule=None):
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
    return learn_runner.run(experiment_fn, output_dir, schedule)

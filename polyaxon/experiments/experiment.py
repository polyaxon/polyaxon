# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import math
import time

from tensorflow.contrib.learn.python.learn.experiment import Experiment as TFExperiment
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import basic_session_run_hooks

from polyaxon import Modes
from polyaxon.libs import getters
from polyaxon.libs.utils import new_attr_context
from polyaxon.processing.input_data import create_input_data_fn


class Experiment(TFExperiment):
    """Experiment is a class containing all information needed to train a model.

    After an experiment is created (by passing an Estimator and inputs for
    training and evaluation), an Experiment instance knows how to invoke training
    and eval loops in a sensible fashion for distributed training.


    None of the functions passed to this constructor are executed at construction time.
    They are stored and used when a method is executed which requires it.

    Args:
        estimator: Object implementing Estimator interface.
        train_input_fn: function, returns features and labels for training.
        eval_input_fn: function, returns features and labels for evaluation. If
            `eval_steps` is `None`, this should be configured only to produce for a
            finite number of batches (generally, 1 epoch over the evaluation data).
        train_steps: Perform this many steps of training.  default: None, means train forever.
        eval_steps: `evaluate` runs until input is exhausted (or another exception is raised),
            or for `eval_steps` steps, if specified.
        eval_delay_secs: Start evaluating after waiting for this many seconds.
        continuous_eval_throttle_secs: Do not re-evaluate unless the last evaluation
            was started at least this many seconds ago for continuous_eval().
        delay_workers_by_global_step: if `True` delays training workers based on global step
            instead of time.
        export_strategies: A list of `ExportStrategy`s, or a single one, or None.
        train_steps_per_iteration: (applies only to continuous_train_and_eval).
            Perform this many (integer) number of train steps for each training-evaluation
            iteration. With a small value, the model will be evaluated more frequently
            with more checkpoints saved. If `None`, will use a default value
            (which is smaller than `train_steps` if provided).

    Raises:
        ValueError: if `estimator` does not implement Estimator interface,
                    or if export_strategies has the wrong type.
    """

    def __init__(self,
                 estimator,
                 train_input_fn,
                 eval_input_fn,
                 train_steps=None,
                 eval_steps=10,
                 train_hooks=None,
                 eval_hooks=None,
                 eval_delay_secs=0,
                 continuous_eval_throttle_secs=60,
                 delay_workers_by_global_step=False,
                 export_strategies=None,
                 train_steps_per_iteration=100):

        self._train_hooks = train_hooks[:] if train_hooks else []
        super(Experiment, self).__init__(
            estimator=estimator,
            train_input_fn=train_input_fn,
            eval_input_fn=eval_input_fn,
            train_steps=train_steps,
            eval_steps=eval_steps,
            train_monitors=self._train_hooks,
            eval_hooks=eval_hooks,
            eval_delay_secs=eval_delay_secs,
            continuous_eval_throttle_secs=continuous_eval_throttle_secs,
            delay_workers_by_global_step=delay_workers_by_global_step,
            export_strategies=export_strategies,
            train_steps_per_iteration=train_steps_per_iteration,
        )

    def extend_train_hooks(self, additional_hooks):
        """Extends the hooks for training."""
        self._train_hooks.extend(additional_hooks)

    def _call_train(self, input_fn=None, steps=None, hooks=None, max_steps=None):
        return self._estimator.train(
            input_fn=input_fn, steps=steps, max_steps=max_steps, hooks=hooks)

    def _call_evaluate(self, input_fn=None, steps=None, name=None, checkpoint_path=None,
                       hooks=None):
        return self._estimator.evaluate(
            input_fn=input_fn, steps=steps, name=name, checkpoint_path=checkpoint_path, hooks=hooks)

    def _prepare_train(self, delay_secs):
        start = time.time()

        # Start the server, if needed. It's important to start the server before
        # we (optionally) sleep for the case where no device_filters are set.
        # Otherwise, the servers will wait to connect to each other before starting
        # to train. We might as well start as soon as we can.
        config = self._estimator.config
        if (config.environment != run_config.Environment.LOCAL and
                    config.environment != run_config.Environment.GOOGLE and
                config.cluster_spec and
                config.master):
            self._start_server()

        extra_hooks = []
        if delay_secs is None:
            task_id = self._estimator.config.task_id or 0
            if self._delay_workers_by_global_step:
                # Wait 5500 global steps for the second worker. Each worker waits more
                # then previous one but with a diminishing number of steps.
                waiting_time = int(8000.0 * math.log(task_id + 1))
                extra_hooks.append(basic_session_run_hooks.GlobalStepWaiterHook(waiting_time))
                delay_secs = 0
            else:
                # Wait 5 secs more for each new worker up to 60 secs.
                delay_secs = min(60, task_id * 5)

        if delay_secs > 0:
            elapsed_secs = time.time() - start
            remaining = delay_secs - elapsed_secs
            logging.info("Waiting {} secs before starting training.".format(remaining))
            time.sleep(delay_secs)

        return delay_secs, extra_hooks

    def train(self, delay_secs=None):
        """Fit the estimator using the training data.

        Train the estimator for `self._train_steps` steps, after waiting for `delay_secs` seconds.
        If `self._train_steps` is `None`, train forever.

        Args:
            delay_secs: Start training after this many seconds.

        Returns:
            The trained estimator.
        """
        delay_secs, extra_hooks = self._prepare_train(delay_secs)
        return self._call_train(input_fn=self._train_input_fn,
                                max_steps=self._train_steps,
                                hooks=self._train_hooks + extra_hooks)

    def evaluate(self, delay_secs=None):
        """Evaluate on the evaluation data.

        Runs evaluation on the evaluation data and returns the result. Runs for
        `self._eval_steps` steps, or if it's `None`, then run until input is
        exhausted or another exception is raised. Start the evaluation after
        `delay_secs` seconds, or if it's `None`, defaults to using
        `self._eval_delay_secs` seconds.

        Args:
            delay_secs: Start evaluating after this many seconds. If `None`, defaults to using
                `self._eval_delays_secs`.

        Returns:
            The result of the `evaluate` call to the `Estimator`.
        """
        super(Experiment, self).evaluate(delay_secs=delay_secs)

    def train_and_evaluate(self):
        """Interleaves training and evaluation.

        The frequency of evaluation is controlled by the constructor arg `eval_every_n_steps`.
        When this parameter is None or 0, evaluation happens only after training has completed.
        Note that evaluation cannot happen more frequently than checkpoints are taken.
        If no new snapshots are available when evaluation is supposed to occur,
        then evaluation doesn't happen for another `eval_every_n_steps` steps
        (assuming a checkpoint is available at that point).
        Thus, settings `eval_every_n_steps` to 1 means that the model will be evaluated
        everytime there is a new checkpoint.

        This is particular useful for a "Master" task in the cloud, whose responsibility
        it is to take checkpoints, evaluate those checkpoints, and write out summaries.
        Participating in training as the supervisor allows such a task to accomplish
        the first and last items, while performing evaluation allows for the second.

        Returns:
            The result of the `evaluate` call to the `Estimator` as well as the
            export results using the specified `ExportStrategy`.
        """
        # The directory to which evaluation summaries are written are determined
        # by adding a suffix to 'eval'; that suffix is the 'name' parameter to
        # the various evaluate(...) methods. By setting it to None, we force
        # the directory name to simply be 'eval'.
        eval_dir_suffix = None

        # We set every_n_steps to 1, but evaluation only occurs when a new
        # snapshot is available. If, by the time we finish evaluation
        # there is a new snapshot, then we just evaluate again. Otherwise,
        # we keep training until one becomes available.
        with new_attr_context(self, "_train_hooks"):
            self._train_hooks = self._train_hooks or []
            # if self._eval_every_n_steps:
            #     self._train_hooks += [monitors.ValidationMonitor(
            #         input_fn=self._eval_input_fn, eval_steps=self._eval_steps,
            #         every_n_steps=self._eval_every_n_steps,
            #         name=eval_dir_suffix, hooks=self._eval_hooks
            #     )]
            self.train(delay_secs=0)

        eval_result = self._call_evaluate(input_fn=self._eval_input_fn,
                                          steps=self._eval_steps,
                                          name=eval_dir_suffix,
                                          hooks=self._eval_hooks)
        return eval_result, self._maybe_export(eval_result)

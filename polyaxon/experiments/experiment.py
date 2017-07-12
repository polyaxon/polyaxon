# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import math
import os
import time

from tensorflow.contrib.learn.python.learn import export_strategy
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.python.framework import ops
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import basic_session_run_hooks, saver, server_lib
from tensorflow.python.util import compat

from polyaxon import Modes
from polyaxon.estimators.estimator import Estimator
from polyaxon.libs import getters
from polyaxon.libs.utils import new_attr_context
from polyaxon.processing.input_data import create_input_data_fn


class Experiment(object):
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
        train_hooks: A list of monitors to pass to the `Estimator`'s `fit` function.
        eval_hooks: A list of `SessionRunHook` hooks to pass to
            the `Estimator`'s `evaluate` function.
        eval_delay_secs: Start evaluating after waiting for this many seconds.
        continuous_eval_throttle_secs: Do not re-evaluate unless the last evaluation
            was started at least this many seconds ago for continuous_eval().
        eval_every_n_steps: (applies only to train_and_evaluate).
            the minimum number of steps between evaluations. Of course, evaluation does not
            occur if no new snapshot is available, hence, this is the minimum.
        delay_workers_by_global_step: if `True` delays training workers based on global step
            instead of time.
        export_strategies: A list of `ExportStrategy`s, or a single one, or None.
        train_steps_per_iteration: (applies only to continuous_train_and_evaluate).
            Perform this many (integer) number of train steps for each training-evaluation
            iteration. With a small value, the model will be evaluated more frequently
            with more checkpoints saved. If `None`, will use a default value
            (which is smaller than `train_steps` if provided).

    Raises:
        ValueError: if `estimator` does not implement Estimator interface,
                    or if export_strategies has the wrong type.
    """

    def __init__(self, estimator, train_input_fn, eval_input_fn, train_steps=None, eval_steps=10,
                 train_hooks=None, eval_hooks=None, eval_delay_secs=0,
                 continuous_eval_throttle_secs=60, eval_every_n_steps=1,
                 delay_workers_by_global_step=False, export_strategies=None,
                 train_steps_per_iteration=100):
        if not isinstance(estimator, Estimator):
            raise ValueError("`estimator` must implement `Estimator`.")

        super(Experiment, self).__init__()
        # Immutable fields.
        self._estimator = estimator
        self._train_steps = train_steps
        self._eval_steps = eval_steps
        self._set_export_strategies(export_strategies)
        self._train_hooks = train_hooks[:] if train_hooks else []
        self._eval_hooks = eval_hooks[:] if eval_hooks else []
        self._train_input_fn = train_input_fn
        self._eval_input_fn = eval_input_fn
        self._eval_delay_secs = eval_delay_secs
        self._continuous_eval_throttle_secs = continuous_eval_throttle_secs
        self._eval_every_n_steps = eval_every_n_steps
        self._delay_workers_by_global_step = delay_workers_by_global_step

        if train_steps_per_iteration is not None and not isinstance(train_steps_per_iteration, int):
            raise ValueError("`train_steps_per_iteration` must be an integer.")
        self._train_steps_per_iteration = train_steps_per_iteration

    @property
    def estimator(self):
        return self._estimator

    @property
    def train_steps(self):
        return self._train_steps

    @property
    def eval_steps(self):
        return self._eval_steps

    def _set_export_strategies(self, values):  # pylint: disable=missing-docstring
        export_strategies = []
        if not values:
            self._export_strategies = ()
            return

        if isinstance(values, export_strategy.ExportStrategy):
            export_strategies.append(values)
        else:
            for value in values:
                if not isinstance(value, export_strategy.ExportStrategy):
                    raise ValueError(
                        "`export_strategies` must be an ExportStrategy, an iterable of "
                        "ExportStrategy, or `None`, found {}.".format(value))
                export_strategies.append(value)
        self._export_strategies = tuple(export_strategies)

    def reset_export_strategies(self, new_export_strategies=None):
        """Resets the export strategies with the `new_export_strategies`.

        Args:
            new_export_strategies: A new list of `ExportStrategy`s, or a single one,
            or None.

        Returns:
            The old export strategies.
        """
        old_export_strategies = self._export_strategies
        self._set_export_strategies(new_export_strategies)
        return old_export_strategies

    def extend_train_hooks(self, additional_hooks):
        """Extends the hooks for training."""
        self._train_hooks.extend(additional_hooks)

    def extend_eval_hooks(self, additional_hooks):
        """Extends the hooks for training."""
        self._eval_hooks.extend(additional_hooks)

    def _start_server(self):
        """Creates, starts, and returns a server_lib.Server."""
        config = self._estimator.config
        if (not config.cluster_spec or not config.task_type or
                not config.master or config.task_id is None):
            raise ValueError("Could not start server; be sure to specify "
                             "cluster_spec, task_type, master, and task in "
                             "RunConfig or set the TF_CONFIG environment variable.")
        server = server_lib.Server(config.cluster_spec, job_name=config.task_type,
                                   task_index=config.task_id, config=config.tf_config, start=False)
        server.start()
        return server

    def _call_train(self, input_fn=None, steps=None, hooks=None, max_steps=None):
        return self._estimator.train(
            input_fn=input_fn, steps=steps, max_steps=max_steps, hooks=hooks)

    def _call_evaluate(self, input_fn=None, steps=None, name=None, checkpoint_path=None,
                       hooks=None):
        return self._estimator.evaluate(
            input_fn=input_fn, steps=steps, name=name, checkpoint_path=checkpoint_path, hooks=hooks)

    def _has_training_stopped(self, eval_result):
        """Determines whether the training has stopped."""
        if not eval_result:
            return False

        global_step = eval_result.get(ops.GraphKeys.GLOBAL_STEP)
        return global_step and self._train_steps and global_step >= self._train_steps

    def _continuous_eval(self, input_fn, name, delay_secs, throttle_delay_secs,
                         evaluate_checkpoint_only_once=True, continuous_eval_predicate_fn=None):
        """Run continuous eval.

        Runs infinite eval on the evaluation data set. This function starts
        evaluating after `delay_secs` seconds and then runs no more than one
        evaluation (with `self._eval_steps` steps each time) per
        `throttle_delay_secs`. If `train_steps` is not None, will return after
        global_step reaches `train_steps`.

        Args:
            input_fn: The input to use for this eval.
            name: A string appended to the folder name of evaluation results.
            delay_secs: Start evaluating after this many seconds.
                If None, defaults to self._eval_delay_secs.
            throttle_delay_secs: Do not re-evaluate unless the last evaluation was started at least
                this many seconds ago. If None, defaults to self._continuous_eval_throttle_secs.
            evaluate_checkpoint_only_once: Whether to skip evaluation of checkpoints that have
                already been evaluated. Default is `True`.
            continuous_eval_predicate_fn: A predicate function determining whether to continue eval
                after each iteration. `predicate_fn` takes the evaluation results as arguments.
                At the beginning of evaluation, the passed eval results will be None
                so it's expected that the predicate function handles that gracefully.
                When `predicate_fn` is not specified, continuous eval will run in an infinite loop
                (if `train_steps` is None) or exit once global step reaches `train_steps`.

        Raises:
            ValueError: if `continuous_eval_predicate_fn` is neither None nor callable.
        """
        if continuous_eval_predicate_fn is not None and not callable(continuous_eval_predicate_fn):
            raise ValueError("`continuous_eval_predicate_fn` must be a callable, or None.")

        if delay_secs is None:
            delay_secs = self._eval_delay_secs
        if throttle_delay_secs is None:
            throttle_delay_secs = self._continuous_eval_throttle_secs

        if delay_secs:
            logging.info("Waiting {} secs before starting eval.".format(delay_secs))
            time.sleep(delay_secs)

        previous_path = None
        eval_result = None
        last_warning_time = 0
        while not continuous_eval_predicate_fn or continuous_eval_predicate_fn(eval_result):
            # Exit if we have already reached number of steps to train.
            if self._has_training_stopped(eval_result):
                logging.info("Exiting continuous eval, global_step={} >= train_step={}".format(
                             eval_result[ops.GraphKeys.GLOBAL_STEP],
                             self._train_steps))
                return

            start = time.time()

            error_msg = None
            latest_path = saver.latest_checkpoint(self._estimator.model_dir)
            if not latest_path:
                error_msg = "Estimator is not fitted yet. " \
                            "Will start an evaluation when a checkpoint is ready."
            elif evaluate_checkpoint_only_once and latest_path == previous_path:
                error_msg = "No new checkpoint ready for evaluation."

            if error_msg:
                # Print warning message every 10 mins.
                eval_result = {}
                if time.time() - last_warning_time > 600:
                    logging.warning(error_msg)
                    last_warning_time = time.time()
            else:
                eval_result = self._call_evaluate(input_fn=input_fn,
                                                  steps=self._eval_steps,
                                                  name=name,
                                                  checkpoint_path=latest_path,
                                                  hooks=self._eval_hooks)
                # Ensure eval result is not None for next round of evaluation.
                if not eval_result:
                    eval_result = {}

                self._maybe_export(eval_result, checkpoint_path=latest_path)

                # Clear warning timer and update last evaluated checkpoint
                last_warning_time = 0
                previous_path = latest_path

            duration = time.time() - start
            if duration < throttle_delay_secs:
                difference = throttle_delay_secs - duration
                logging.info("Waiting {} secs before starting next eval run.".format(difference))
                time.sleep(difference)

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
        if delay_secs is None:
            delay_secs = self._eval_delay_secs

        if delay_secs:
            logging.info("Waiting {} secs before starting eval.".format(delay_secs))
            time.sleep(delay_secs)

        return self._call_evaluate(input_fn=self._eval_input_fn,
                                   steps=self._eval_steps,
                                   name="one_pass",
                                   hooks=self._eval_hooks)

    def continuous_eval(self,
                        delay_secs=None,
                        throttle_delay_secs=None,
                        evaluate_checkpoint_only_once=True,
                        continuous_eval_predicate_fn=None):
        self._continuous_eval(
            self._eval_input_fn,
            name="continuous",
            delay_secs=delay_secs,
            throttle_delay_secs=throttle_delay_secs,
            evaluate_checkpoint_only_once=evaluate_checkpoint_only_once,
            continuous_eval_predicate_fn=continuous_eval_predicate_fn)

    def continuous_eval_on_train_data(self,
                                      delay_secs=None,
                                      throttle_delay_secs=None,
                                      continuous_eval_predicate_fn=None):
        self._continuous_eval(
            self._train_input_fn,
            name="continuous_on_train_data",
            delay_secs=delay_secs,
            throttle_delay_secs=throttle_delay_secs,
            continuous_eval_predicate_fn=continuous_eval_predicate_fn)

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
                # self._train_hooks += [monitors.ValidationMonitor(
                #     input_fn=self._eval_input_fn, eval_steps=self._eval_steps,
                #     every_n_steps=self._eval_every_n_steps,
                #     name=eval_dir_suffix, hooks=self._eval_hooks
                # )]
            self.train(delay_secs=0)

        eval_result = self._call_evaluate(input_fn=self._eval_input_fn,
                                          steps=self._eval_steps,
                                          name=eval_dir_suffix,
                                          hooks=self._eval_hooks)
        return eval_result, self._maybe_export(eval_result)

    def continuous_train_and_evaluate(self, continuous_eval_predicate_fn=None):
        """Interleaves training and evaluation.

        The frequency of evaluation is controlled by the `train_steps_per_iteration`
        (via constructor). The model will be first trained for
        `train_steps_per_iteration`, and then be evaluated in turns.

        This differs from `train_and_evaluate` as follows:
            1. The procedure will have train and evaluation in turns. The model
            will be trained for a number of steps (usuallly smaller than `train_steps`
            if provided) and then be evaluated.  `train_and_evaluate` will train the
            model for `train_steps` (no small training iteraions).

            2. Due to the different approach this schedule takes, it leads to two
            differences in resource control. First, the resources (e.g., memory) used
            by training will be released before evaluation (`train_and_evaluate` takes
            double resources). Second, more checkpoints will be saved as a checkpoint
            is generated at the end of each small trainning iteration.

        Args:
            continuous_eval_predicate_fn: A predicate function determining whether to
            continue after each iteration. `predicate_fn` takes the evaluation
            results as its arguments. At the beginning of evaluation, the passed
            eval results will be None so it's expected that the predicate function
            handles that gracefully. When `predicate_fn` is not specified, this will
            run in an infinite loop or exit when global_step reaches `train_steps`.

        Returns:
           A tuple of the result of the `evaluate` call to the `Estimator` and the
           export results using the specified `ExportStrategy`.

        Raises:
            ValueError: if `continuous_eval_predicate_fn` is neither None norcallable.
        """

        if (continuous_eval_predicate_fn is not None and
                not callable(continuous_eval_predicate_fn)):
            raise ValueError("`continuous_eval_predicate_fn` must be a callable, or None.")

        eval_result = None

        # Set the default value for train_steps_per_iteration, which will be
        # overriden by other settings.
        train_steps_per_iteration = 1000
        if self._train_steps_per_iteration is not None:
            train_steps_per_iteration = self._train_steps_per_iteration
        elif self._train_steps is not None:
            train_steps_per_iteration = int(self._train_steps / 10)

        while not continuous_eval_predicate_fn or continuous_eval_predicate_fn(eval_result):

            if self._has_training_stopped(eval_result):
                # Exits once max steps of training is satisfied.
                logging.info("Stop training model as max steps reached")
                break

            logging.info("Training model for {} steps".format(train_steps_per_iteration))
            self._call_train(input_fn=self._train_input_fn,
                             steps=train_steps_per_iteration,
                             hooks=self._train_hooks)

            logging.info("Evaluating model now.")
            eval_result = self._call_evaluate(input_fn=self._eval_input_fn,
                                              steps=self._eval_steps,
                                              name="one_pass",
                                              hooks=self._eval_hooks)

        return eval_result, self._maybe_export(eval_result)

    def _maybe_export(self, eval_result, checkpoint_path=None):
        """Export the Estimator using export_fn, if defined."""
        export_dir_base = os.path.join(compat.as_bytes(self._estimator.model_dir),
                                       compat.as_bytes("export"))

        export_results = []
        for strategy in self._export_strategies:
            export_path = os.path.join(compat.as_bytes(export_dir_base),
                                       compat.as_bytes(strategy.name))
            export_results.append(
                strategy.export(self._estimator, export_path=export_path,
                                checkpoint_path=checkpoint_path, eval_result=eval_result))

        return export_results

    def run_std_server(self):
        """Starts a TensorFlow server and joins the serving thread.

        Typically used for parameter servers.

        Raises:
            ValueError: if not enough information is available in the estimator's
            config to create a server.
        """
        self._start_server().join()

    def test(self):
        """Tests training, evaluating and exporting the estimator for a single step.

        Returns:
            The result of the `evaluate` call to the `Estimator`.
        """
        self._call_train(input_fn=self._train_input_fn, steps=1, hooks=self._train_hooks)
        eval_result = self._call_evaluate(input_fn=self._eval_input_fn, steps=1, name="one_pass")
        _ = self._maybe_export(eval_result)
        return eval_result


def create_experiment(experiment_config):
    """Creates a new `Experiment` instance.

    Args:
        experiment_config: the config to use for creating the experiment.
    """
    # Creates training input function
    train_input_data_config = experiment_config.train_input_data_config
    train_input_fn = create_input_data_fn(
        pipeline_config=train_input_data_config.pipeline_config,
        mode=Modes.TRAIN, scope='train_input_fn',
        input_type=train_input_data_config.input_type,
        x=train_input_data_config.x, y=train_input_data_config.y)

    # Creates eval_input_fn input function
    eval_input_data_config = experiment_config.eval_input_data_config
    eval_input_fn = create_input_data_fn(
        pipeline_config=eval_input_data_config.pipeline_config,
        mode=Modes.EVAL, scope='eval_input_fn',
        input_type=eval_input_data_config.input_type,
        x=eval_input_data_config.x, y=eval_input_data_config.y)

    estimator = getters.get_estimator(experiment_config.estimator_config,
                                      experiment_config.model_config,
                                      experiment_config.run_config)
    train_hooks = getters.get_hooks(experiment_config.train_hooks_config)
    eval_hooks = getters.get_hooks(experiment_config.eval_hooks_config)

    experiment = Experiment(
        estimator=estimator,
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=experiment_config.train_steps,
        eval_steps=experiment_config.eval_steps,
        train_hooks=train_hooks,
        eval_hooks=eval_hooks,
        eval_delay_secs=experiment_config.eval_delay_secs,
        continuous_eval_throttle_secs=experiment_config.continuous_eval_throttle_secs,
        eval_every_n_steps=experiment_config.eval_every_n_steps,
        delay_workers_by_global_step=experiment_config.delay_workers_by_global_step,
        export_strategies=experiment_config.export_strategies,
        train_steps_per_iteration=experiment_config.train_steps_per_iteration)

    return experiment

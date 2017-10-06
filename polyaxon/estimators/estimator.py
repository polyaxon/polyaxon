# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six
from six.moves import xrange

from tensorflow.contrib.framework import list_variables, load_variable
from tensorflow.core.protobuf import config_pb2
from tensorflow.python.estimator import estimator as tf_estimator
from tensorflow.python.framework import ops, random_seed
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import (
    monitored_session,
    saver,
    training
)
from tensorflow.python.training.session_run_hook import SessionRunHook

from polyaxon import Modes
from polyaxon.estimators.estimator_spec import EstimatorSpec
from polyaxon.estimators import hooks as plx_hooks
from polyaxon.estimators.run_config import RunConfig
from polyaxon.libs.exceptions import EstimatorNotTrainedError
from polyaxon.libs.utils import extract_batch_length, generate_model_dir, get_arguments


class Estimator(tf_estimator.Estimator):
    """Estimator class is a model trainer/evaluator.

    Constructs an `Estimator` instance.

    Args:
        model_fn: Model function. Follows the signature:
            * Args:
                * `features`: single `Tensor` or `dict` of `Tensor`s
                     (depending on data passed to `fit`),
                * `labels`: `Tensor` or `dict` of `Tensor`s (for multi-head models).
                    If mode is `Modes.PREDICT`, `labels=None` will be passed.
                    If the `model_fn`'s signature does not accept `mode`,
                    the `model_fn` must still be able to handle `labels=None`.
                * `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
                * `params`: Optional `dict` of hyperparameters.  Will receive what
                    is passed to Estimator in `params` parameter. This allows
                    to configure Estimators from hyper parameter tuning.
                * `config`: Optional configuration object. Will receive what is passed
                    to Estimator in `config` parameter, or the default `config`.
                    Allows updating things in your model_fn based on configuration
                    such as `num_ps_replicas`.
                * `model_dir`: Optional directory where model parameters, graph etc
                    are saved. Will receive what is passed to Estimator in
                    `model_dir` parameter, or the default `model_dir`. Allows
                    updating things in your model_fn that expect model_dir, such as
                    training hooks.

            * Returns:
               `EstimatorSpec`

            Supports next three signatures for the function:

                * `(features, labels, mode)`
                * `(features, labels, mode, params)`
                * `(features, labels, mode, params, config)`
                * `(features, labels, mode, params, config, model_dir)`

        model_dir: Directory to save model parameters, graph and etc. This can
            also be used to load checkpoints from the directory into a estimator to
            continue training a previously saved model.
        config: Configuration object.
        params: `dict` of hyper parameters that will be passed into `model_fn`.
                  Keys are names of parameters, values are basic python types.
    Raises:
        ValueError: parameters of `model_fn` don't match `params`.
    """

    # pylint: disable=super-init-not-called
    def __init__(self, model_fn, model_dir=None, config=None, params=None):
        # Create a run configuration.
        if config is None:
            self._config = RunConfig()
            logging.info("Using default config.")
        else:
            if not isinstance(config, RunConfig):
                raise ValueError("config must be an instance of RunConfig, "
                                 "received {}.".format(config))
            self._config = config

        if(model_dir is not None) and (self._config.model_dir is not None):
            if model_dir != self._config.model_dir:
                raise ValueError(
                    "model_dir are set both in constructor and RunConfig, but with "
                    "different values. In constructor: '{}', in RunConfig: "
                    "'{}' ".format(model_dir, self._config.model_dir))

        self._model_dir = model_dir or self._config.model_dir or generate_model_dir()
        if self._config.model_dir is None:
            self._config = self._config.replace(model_dir=self._model_dir)
        logging.info("Using config: {}".format(vars(self._config)))

        if self._config.session_config is None:
            self._session_config = config_pb2.ConfigProto(allow_soft_placement=True)
        else:
            self._session_config = self._config.session_config

        # Set device function depending if there are replicas or not.
        # pylint: disable=protected-access
        self._device_fn = tf_estimator._get_replica_device_setter(self._config)

        tf_estimator._verify_model_fn_args(model_fn, params)  # pylint: disable=protected-access

        self._model_fn = model_fn
        self._params = params or {}

    def train(self,  # pylint: disable=arguments-differ
              nput_fn=None, steps=None, hooks=None, max_steps=None):
        """Trains a model given training data `x` predictions and `y` labels.

        Args:
            input_fn: Input function returning a tuple of:
                features - `Tensor` or dictionary of string feature name to `Tensor`.
                labels - `Tensor` or dictionary of `Tensor` with labels.
            steps: Number of steps for which to train model. If `None`, train forever.
                'steps' works incrementally. If you call two times fit(steps=10) then
                training occurs in total 20 steps. If you don't want to have incremental
                behaviour please set `max_steps` instead. If set, `max_steps` must be
                `None`.
            hooks: List of `BaseMonitor` subclass instances.
                Used for callbacks inside the training loop.
            max_steps: Number of total steps for which to train model. If `None`,
                train forever. If set, `steps` must be `None`.

            Two calls to `fit(steps=100)` means 200 training iterations.
            On the other hand, two calls to `fit(max_steps=100)` means
            that the second call will not do any iteration since first call did all 100 steps.

        Returns:
            `self`, for chaining.
        """
        if max_steps is not None:
            try:
                start_step = load_variable(self._model_dir, ops.GraphKeys.GLOBAL_STEP)
                if max_steps <= start_step:
                    logging.info('Skipping training since max_steps has already saved.')
                    return self
            except:  # pylint: disable=bare-except
                pass

        hooks = self._prepare_train(steps, hooks, max_steps)
        loss = self._train_model(input_fn=input_fn, hooks=hooks)
        logging.info('Loss for final step: %s.', loss)
        return self

    def evaluate(self, input_fn=None, steps=None, hooks=None, checkpoint_path=None, name=None):
        """Evaluates given model with provided evaluation data.

        Stop conditions - we evaluate on the given input data until one of the
        following:
        - If `steps` is provided, and `steps` batches of size `batch_size` are processed.
        - If `input_fn` is provided, and it raises an end-of-input
        exception (`OutOfRangeError` or `StopIteration`).
        - If `x` is provided, and all items in `x` have been processed.

        Args:
            input_fn: Input function returning a tuple of:
                features - Dictionary of string feature name to `Tensor` or `Tensor`.
                labels - `Tensor` or dictionary of `Tensor` with labels.
                If `steps` is not provided, this should raise `OutOfRangeError` or
                `StopIteration` after the desired amount of data (e.g., one epoch) has
                been provided. See "Stop conditions" above for specifics.
            steps: Number of steps for which to evaluate model. If `None`, evaluate
                until `x` is consumed or `input_fn` raises an end-of-input exception.
                See "Stop conditions" above for specifics.
            checkpoint_path: Path of a specific checkpoint to evaluate. If `None`,
                the latest checkpoint in `model_dir` is used.
            hooks: List of `SessionRunHook` subclass instances.
                Used for callbacks inside the evaluation call.
            name: Name of the evaluation if user needs to run multiple evaluations on
                different data sets, such as on training data vs test data.

        Raises:
            ValueError: If `metrics` is not `None` or `dict`.

        Returns:
            Returns `dict` with evaluation results; the metrics specified in `metrics`, as
            well as an entry `global_step` which contains the value of the global step
            for which this evaluation was performed.
        """
        hooks = self._check_hooks(hooks)
        if steps is not None:
            if steps <= 0:
                raise ValueError('Must specify steps > 0, given: {}'.format(steps))
            hooks.append(plx_hooks.StopAfterNEvalsHook(num_evals=steps))
        try:
            return self._evaluate_model(
                input_fn=input_fn, name=name, checkpoint_path=checkpoint_path, hooks=hooks)
        except ValueError as e:
            raise EstimatorNotTrainedError(e)

    def predict(self, input_fn=None, predict_keys=None, hooks=None, checkpoint_path=None):
        """Returns predictions for given features with `PREDICT` mode.

        Args:
            input_fn: Input function returning features which is a dictionary of
                string feature name to `Tensor` or `SparseTensor`. If it returns a
                tuple, first item is extracted as features. Prediction continues until
                `input_fn` raises an end-of-input exception (`OutOfRangeError` or `StopIteration`).
            predict_keys: list of `str`, name of the keys to predict. It is used if
                the `EstimatorSpec.predictions` is a `dict`. If `predict_keys` is used then rest
                of the predictions will be filtered from the dictionary. If `None`, returns all.
            hooks: List of `SessionRunHook` subclass instances. Used for callbacks
                inside the prediction call.
            checkpoint_path: Path of a specific checkpoint to predict. If `None`, the
                latest checkpoint in `model_dir` is used.

        Yields:
            Evaluated values of `predictions` tensors.

        Raises:
            ValueError: Could not find a trained model in model_dir.
            ValueError: if batch length of predictions are not same.
            ValueError: If there is a conflict between `predict_keys` and `predictions`.
                For example if `predict_keys` is not `None`
                but `EstimatorSpec.predictions` is not a `dict`.
        """
        return self._infer_model(Modes.PREDICT, input_fn=input_fn, predict_keys=predict_keys,
                                 hooks=hooks, checkpoint_path=checkpoint_path)

    def generate(self, input_fn=None, predict_keys=None, hooks=None, checkpoint_path=None):
        """Returns predictions for given features with `GENERATE` mode.

        Args:
            input_fn: Input function returning features which is a dictionary of
                string feature name to `Tensor` or `SparseTensor`. If it returns a
                tuple, first item is extracted as features. Prediction continues until
                `input_fn` raises an end-of-input exception (`OutOfRangeError` or `StopIteration`).
            predict_keys: list of `str`, name of the keys to predict. It is used if
                the `EstimatorSpec.predictions` is a `dict`. If `predict_keys` is used then rest
                of the predictions will be filtered from the dictionary. If `None`, returns all.
            hooks: List of `SessionRunHook` subclass instances. Used for callbacks
                inside the prediction call.
            checkpoint_path: Path of a specific checkpoint to predict. If `None`, the
                latest checkpoint in `model_dir` is used.

        Yields:
            Evaluated values of `predictions` tensors.

        Raises:
            ValueError: Could not find a trained model in model_dir.
            ValueError: if batch length of predictions are not same.
            ValueError: If there is a conflict between `predict_keys` and `predictions`.
                For example if `predict_keys` is not `None`
                but `EstimatorSpec.predictions` is not a `dict`.
        """
        return self._infer_model(Modes.GENERATE, input_fn=input_fn, predict_keys=predict_keys,
                                 hooks=hooks, checkpoint_path=checkpoint_path)

    def encode(self, input_fn=None, predict_keys=None, hooks=None, checkpoint_path=None):
        """Returns predictions for given features with `ENCODE` mode.

        Args:
            input_fn: Input function returning features which is a dictionary of
                string feature name to `Tensor` or `SparseTensor`. If it returns a
                tuple, first item is extracted as features. Prediction continues until
                `input_fn` raises an end-of-input exception (`OutOfRangeError` or `StopIteration`).
            predict_keys: list of `str`, name of the keys to predict. It is used if
                the `EstimatorSpec.predictions` is a `dict`. If `predict_keys` is used then rest
                of the predictions will be filtered from the dictionary. If `None`, returns all.
            hooks: List of `SessionRunHook` subclass instances. Used for callbacks
                inside the prediction call.
            checkpoint_path: Path of a specific checkpoint to predict. If `None`, the
                latest checkpoint in `model_dir` is used.

        Yields:
            Evaluated values of `predictions` tensors.

        Raises:
            ValueError: Could not find a trained model in model_dir.
            ValueError: if batch length of predictions are not same.
            ValueError: If there is a conflict between `predict_keys` and `predictions`.
                For example if `predict_keys` is not `None`
                but `EstimatorSpec.predictions` is not a `dict`.
        """
        return self._infer_model(Modes.ENCODE, input_fn=input_fn, predict_keys=predict_keys,
                                 hooks=hooks, checkpoint_path=checkpoint_path)

    def get_variable_value(self, name):
        """Returns value of the variable given by name.

        Args:
            name: string, name of the tensor.

        Returns:
            Numpy array - value of the tensor.
        """
        return load_variable(self.model_dir, name)

    def get_variable_names(self):
        """Returns list of all variable names in this model.

        Returns:
            List of names.
        """
        return [name for name, _ in list_variables(self.model_dir)]

    @staticmethod
    def _verify_model_fn_args(model_fn, params):
        """Verifies model fn arguments."""

        valid_model_fn_args = {'features', 'labels', 'mode', 'params', 'config'}

        if model_fn is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(model_fn)
            if 'features' not in model_fn_args:
                raise ValueError('model_fn `{}` must include features argument.'.format(model_fn))
            if 'labels' not in model_fn_args:
                raise ValueError('model_fn `{}` must include labels argument.'.format(model_fn))

            if params is not None and 'params' not in model_fn_args:
                raise ValueError("Estimator's model_fn `{}` does not include params argument, "
                                 "but params `{}` are passed.".format(model_fn, params))
            if params is None and 'params' in model_fn_args:
                logging.warning("Estimator's model_fn (%s) includes params "
                                "argument, but params are not passed to Estimator.", model_fn)
        else:
            raise ValueError("`model_fn` must be provided to Estimator.")

        if 'self' in model_fn_args:
            model_fn_args.remove('self')

        non_valid_args = set(model_fn_args) - valid_model_fn_args
        if non_valid_args:
            raise ValueError("model_fn `{}` has following not expected args: {}".format(
                model_fn, non_valid_args))

    @staticmethod
    def _check_hooks(hooks):
        """Returns hooks if all are SessionRunHook, raises TypeError otherwise."""
        hooks = list(hooks or [])
        for h in hooks:
            if not isinstance(h, SessionRunHook):
                raise TypeError("Hooks must be a SessionRunHook, given: {}".format(h))

        return hooks

    def _prepare_train(self, steps=None, hooks=None, max_steps=None):
        """Checks train specifications (steps and hooks) and return the train hooks.

        Args:
            steps: Number of steps for which to train model. If `None`, train forever.
                'steps' works incrementally. If you call two times fit(steps=10) then
                training occurs in total 20 steps. If you don't want to have incremental
                behaviour please set `max_steps` instead. If set, `max_steps` must be
                `None`.
            hooks: List of `BaseMonitor` subclass instances.
                Used for callbacks inside the training loop.
            max_steps: Number of total steps for which to train model. If `None`,
                train forever. If set, `steps` must be `None`.

        Returns:
            `list`: An updated version of hooks.
        """
        if (steps is not None) and (max_steps is not None):
            raise ValueError("Can not provide both steps and max_steps.")
        if steps is not None and steps <= 0:
            raise ValueError("Must specify steps > 0, given: {}".format(steps))
        if max_steps is not None and max_steps <= 0:
            raise ValueError("Must specify max_steps > 0, given: {}".format(max_steps))

        hooks = self._check_hooks(hooks)
        if steps is not None or max_steps is not None:
            hooks.append(plx_hooks.StopAtStepHook(steps, max_steps))

        return hooks

    def _call_model_fn(self, features, labels, mode):
        """Calls model function.

        Args:
          features: features dict.
          labels: labels dict.
          mode: ModeKeys

        Returns:
          An `EstimatorSpec` object.

        Raises:
          ValueError: if model_fn returns invalid objects.
        """
        model_fn_args = get_arguments(self._model_fn)
        kwargs = {}
        if 'labels' in model_fn_args:
            kwargs['labels'] = labels
        else:
            if labels is not None:
                raise ValueError(
                    'model_fn does not take labels, but input_fn returns labels.')
        if 'mode' in model_fn_args:
            kwargs['mode'] = mode
        if 'params' in model_fn_args:
            kwargs['params'] = self.params
        if 'config' in model_fn_args:
            kwargs['config'] = self.config
        model_fn_results = self._model_fn(features=features, **kwargs)

        if not isinstance(model_fn_results, EstimatorSpec):
            raise ValueError('model_fn should return an EstimatorSpec.')

        return model_fn_results

    @staticmethod
    def _extract_metric_update_ops(eval_dict):
        """Separate update operations from metric value operations."""
        update_ops = []
        value_ops = {}
        # Sort metrics lexicographically so graph is identical every time.
        for name, metric_ops in sorted(six.iteritems(eval_dict)):
            value_ops[name] = metric_ops[0]
            update_ops.append(metric_ops[1])

        if update_ops:
            update_op = control_flow_ops.group(*update_ops)
        else:
            update_op = None

        return update_op, value_ops

    def _train_model(self, input_fn, hooks):
        all_hooks = []
        with ops.Graph().as_default() as g, g.device(self._device_fn):
            random_seed.set_random_seed(self._config.tf_random_seed)
            global_step = training.get_or_create_global_step(g)
            features, labels = self._get_features_and_labels_from_input_fn(input_fn, Modes.TRAIN)
            estimator_spec = self._call_model_fn(features, labels, Modes.TRAIN)
            ops.add_to_collection(ops.GraphKeys.LOSSES, estimator_spec.loss)
            all_hooks.extend([
                plx_hooks.NanTensorHook(estimator_spec.loss),
                plx_hooks.StepLoggingTensorHook(
                    {
                        'loss': estimator_spec.loss,
                        'step': global_step
                    },
                    every_n_iter=100)
            ])
            all_hooks.extend(hooks)
            all_hooks.extend(estimator_spec.training_hooks)

            scaffold = estimator_spec.scaffold
            if not (scaffold.saver or ops.get_collection(ops.GraphKeys.SAVERS)):
                ops.add_to_collection(
                    ops.GraphKeys.SAVERS,  # TODO remove non restorable vars
                    saver.Saver(
                        sharded=True,
                        max_to_keep=self._config.keep_checkpoint_max,
                        keep_checkpoint_every_n_hours=(
                            self._config.keep_checkpoint_every_n_hours),
                        defer_build=True,
                        save_relative_paths=True))

            chief_hooks = []
            if self._config.save_checkpoints_secs or self._config.save_checkpoints_steps:
                saver_hook_exists = any(
                    [isinstance(h, plx_hooks.StepCheckpointSaverHook)
                     for h in (all_hooks +
                               chief_hooks +
                               list(estimator_spec.training_chief_hooks))])
                if not saver_hook_exists:
                    chief_hooks += [
                        plx_hooks.StepCheckpointSaverHook(
                            self._model_dir,
                            save_secs=self._config.save_checkpoints_secs,
                            save_steps=self._config.save_checkpoints_steps,
                            scaffold=scaffold)
                    ]
            if self._config.save_summary_steps:
                saver_hook_exists = any(
                    [isinstance(h, plx_hooks.StepSummarySaverHook)
                     for h in (all_hooks +
                               chief_hooks +
                               list(estimator_spec.training_chief_hooks))])
                if not saver_hook_exists:
                    chief_hooks += [
                        plx_hooks.StepSummarySaverHook(
                            scaffold=scaffold,
                            save_steps=self._config.save_summary_steps,
                            output_dir=self._model_dir,
                        )
                    ]

            with monitored_session.MonitoredTrainingSession(
                  master=self._config.master,
                  is_chief=self._config.is_chief,
                  checkpoint_dir=self._model_dir,
                  scaffold=scaffold,
                  hooks=all_hooks,
                  chief_only_hooks=chief_hooks + list(estimator_spec.training_chief_hooks),
                  save_checkpoint_secs=0,  # Saving checkpoint is handled by a hook.
                  save_summaries_steps=0,  # Saving summaries is handled by a hook.
                  config=self._session_config) as mon_sess:
                loss = None
                while not mon_sess.should_stop():
                    _, loss = mon_sess.run([estimator_spec.train_op, estimator_spec.loss])
            return loss

    def _infer_model(self, mode, input_fn=None, predict_keys=None, hooks=None,
                     checkpoint_path=None):
        """Returns predictions for given features given an inference mode.

        Args:
            mode: The inference to use, possible values: PREDICT, GENERATE, ENCODE.
            input_fn: Input function returning features which is a dictionary of
                string feature name to `Tensor` or `SparseTensor`. If it returns a
                tuple, first item is extracted as features. Prediction continues until
                `input_fn` raises an end-of-input exception (`OutOfRangeError` or `StopIteration`).
            predict_keys: list of `str`, name of the keys to predict. It is used if
                the `EstimatorSpec.predictions` is a `dict`. If `predict_keys` is used then rest
                of the predictions will be filtered from the dictionary. If `None`, returns all.
            hooks: List of `SessionRunHook` subclass instances. Used for callbacks
                inside the prediction call.
            checkpoint_path: Path of a specific checkpoint to predict. If `None`, the
                latest checkpoint in `model_dir` is used.

        Yields:
            Evaluated values of `predictions` tensors.

        Raises:
            ValueError: Could not find a trained model in model_dir.
            ValueError: if batch length of predictions are not same.
            ValueError: If there is a conflict between `predict_keys` and `predictions`.
                For example if `predict_keys` is not `None`
                but `EstimatorSpec.predictions` is not a `dict`.
        """
        hooks = self._check_hooks(hooks)
        # Check that model has been trained.
        if not checkpoint_path:
            checkpoint_path = saver.latest_checkpoint(self._model_dir)
        if not checkpoint_path:
            raise ValueError('Could not find trained model in model_dir: {}.'.format(
                self._model_dir))

        with ops.Graph().as_default() as g:
            random_seed.set_random_seed(self._config.tf_random_seed)
            self._create_and_assert_global_step(g)
            features = self._get_features_from_input_fn(input_fn, mode)
            estimator_spec = self._call_model_fn(features, None, mode)
            predictions = self._extract_keys(estimator_spec.predictions, predict_keys)
            with monitored_session.MonitoredSession(
                  session_creator=monitored_session.ChiefSessionCreator(
                    checkpoint_filename_with_path=checkpoint_path,
                    scaffold=estimator_spec.scaffold,
                    config=self._session_config),
                  hooks=hooks) as mon_sess:
                while not mon_sess.should_stop():
                    preds_evaluated = mon_sess.run(predictions)
                    if not isinstance(predictions, dict):
                        for pred in preds_evaluated:
                            yield pred
                    else:
                        for i in xrange(extract_batch_length(preds_evaluated)):
                            yield {key: value[i] for key, value in six.iteritems(preds_evaluated)}

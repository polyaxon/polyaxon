# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import copy
import os
import six

import numpy as np

from tensorflow.contrib import framework as contrib_framework
from tensorflow.contrib import metrics as metrics_lib
from tensorflow.contrib.framework import list_variables, load_variable
from tensorflow.contrib.framework.python.ops import variables as contrib_variables
from tensorflow.contrib.learn.python.learn.estimators import run_config
from tensorflow.contrib.learn.python.learn.estimators._sklearn import NotFittedError
from tensorflow.contrib.learn.python.learn.estimators.estimator import _get_replica_device_setter
from tensorflow.contrib.learn.python.learn.utils import saved_model_export_utils
from tensorflow.contrib.training.python.training import evaluation
from tensorflow.core.framework import summary_pb2
from tensorflow.core.protobuf import config_pb2
from tensorflow.python.client import session as tf_session
from tensorflow.python.estimator import model_fn as model_fn_lib
from tensorflow.python.framework import ops, random_seed
from tensorflow.python.ops import control_flow_ops, data_flow_ops, resources, variables
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.platform import gfile
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.training import basic_session_run_hooks, monitored_session, saver, summary_io
from tensorflow.python.training.session_run_hook import SessionRunHook
from tensorflow.python.util import compat

from polyaxon.libs.dicts import dict_to_str
from polyaxon.libs.utils import extract_batch_length, generate_model_dir, get_arguments


class Estimator(object):
    """Estimator class is the basic TensorFlow model trainer/evaluator."""

    def __init__(self, model_fn=None, model_dir=None, config=None, params=None):
        """Constructs an `Estimator` instance.

        Args:
            model_fn: Model function. Follows the signature:
                * Args:
                    * `features`: single `Tensor` or `dict` of `Tensor`s
                         (depending on data passed to `fit`),
                    * `labels`: `Tensor` or `dict` of `Tensor`s (for multi-head models).
                        If mode is `ModeKeys.PREDICT`, `labels=None` will be passed.
                        If the `model_fn`'s signature does not accept `mode`,
                        the `model_fn` must still be able to handle `labels=None`.
                    * `mode`: Optional. Specifies if this training, evaluation or prediction.
                        See `ModeKeys`.
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

                    * `(features, labels)`
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
        # Create a run configuration.
        if config is None:
            self._config = run_config.RunConfig()
            logging.info("Using default config.")
        else:
            if not isinstance(config, run_config.RunConfig):
                raise ValueError("config must be an instance of RunConfig, "
                                 "received {}.".format(config))
            self._config = config
        logging.info("Using config: {}".format(vars(self._config)))

        self._model_dir = model_dir or generate_model_dir()
        if self._config.model_dir is None:
            self._config = self._config.replace(model_dir=self._model_dir)

        # if self._config.session_config is None:
        self._session_config = config_pb2.ConfigProto(allow_soft_placement=True)
        # else:
        #     self._session_config = self._config.session_config

        # Set device function depending if there are replicas or not.
        self._device_fn = _get_replica_device_setter(self._config)

        self._graph = None

        if model_fn is not None:
            # Check number of arguments of the given function matches requirements.
            model_fn_args = get_arguments(model_fn)
            if params is not None and 'params' not in model_fn_args:
                raise ValueError("Estimator's model_fn `{}` has less than 4 arguments, "
                                 "but not None params `{}` are passed.".format(model_fn, params))
            if params is None and 'params' in model_fn_args:
                logging.warning("Estimator's model_fn (%s) includes params "
                                "argument, but params are not passed to Estimator.", model_fn)
        else:
            raise ValueError("`model_fn` must be provided to Estimator.")
        self._model_fn = model_fn
        self._params = params or {}

    @property
    def model_dir(self):
        return self._model_dir

    @property
    def config(self):
        return copy.deepcopy(self._config)

    @property
    def params(self):
        return copy.deepcopy(self._params)

    def _call_model_fn(self, features, labels, mode):
        """Calls model function with support of 2, 3 or 4 arguments.

        Args:
            features: features dict.
            labels: labels dict.
            mode: ModeKeys

        Returns:
            A `ModelFnOps` object.
            If model_fn returns a tuple, wraps them up in a `ModelFnOps` object.

        Raises:
            ValueError: if model_fn returns invalid objects.
        """
        model_fn_args = get_arguments(self._model_fn)
        kwargs = {}
        if 'mode' in model_fn_args:
            kwargs['mode'] = mode
        if 'params' in model_fn_args:
            kwargs['params'] = self.params
        if 'config' in model_fn_args:
            kwargs['config'] = self.config
        model_fn_results = self._model_fn(features, labels, **kwargs)

        if not isinstance(model_fn_results, model_fn_lib.EstimatorSpec):
            raise ValueError('model_fn should return an EstimatorSpec.')

        return model_fn_results

    def export_savedmodel(self, export_dir_base, serving_input_fn,
                          default_output_alternative_key=None,
                          assets_extra=None, as_text=False, checkpoint_path=None):
        """Exports inference graph as a SavedModel into given dir.

        Args:
            export_dir_base: A str directory to write the exported graph and checkpoints.
            serving_input_fn: A function that takes no argument and returns an `InputFnOps`.
            default_output_alternative_key: the name of the head to serve when none is specified.
                Not needed for single-headed models.
            assets_extra: A dict specifying how to populate the assets.extra directory
                within the exported SavedModel.  Each key should give the destination
                path (including the filename) relative to the assets.extra directory.
                The corresponding value gives the full path of the source file to be
                copied.  For example, the simple case of copying a single file without
                renaming it is specified as `{'my_asset_file.txt': '/path/to/my_asset_file.txt'}`.
            as_text: whether to write the SavedModel proto in text format.
            checkpoint_path: The checkpoint path to export.  If None (the default),
                the most recent checkpoint found within the model directory is chosen.

        Returns:
          The string path to the exported directory.

        Raises:
          ValueError: if an unrecognized export_type is requested.
        """
        if serving_input_fn is None:
            raise ValueError('serving_input_fn must be defined.')

        with ops.Graph().as_default() as g:
            contrib_variables.create_global_step(g)
            random_seed.set_random_seed(self._config.tf_random_seed)
            # Call the serving_input_fn and collect the input alternatives.
            input_ops = serving_input_fn()
            input_alternatives, features = (
                saved_model_export_utils.get_input_alternatives(input_ops))

            # Call the model_fn and collect the output alternatives.
            estimator_spec = self._call_model_fn(features, None, model_fn_lib.ModeKeys.PREDICT)
            output_alternatives, actual_default_output_alternative_key = (
                saved_model_export_utils.get_output_alternatives(
                    estimator_spec, default_output_alternative_key))

            # Build the SignatureDefs from all pairs of input and output alternatives
            signature_def_map = saved_model_export_utils.build_all_signature_defs(
                input_alternatives, output_alternatives, actual_default_output_alternative_key)

            if not checkpoint_path:
                # Locate the latest checkpoint
                checkpoint_path = saver.latest_checkpoint(self._model_dir)
            if not checkpoint_path:
                raise NotFittedError("Couldn't find trained model at {}.".format(self._model_dir))

            export_dir = saved_model_export_utils.get_timestamped_export_dir(export_dir_base)

            if estimator_spec.scaffold is not None and estimator_spec.scaffold.saver is not None:
                saver_for_restore = estimator_spec.scaffold.saver
            else:
                saver_for_restore = saver.Saver(sharded=True)
            with tf_session.Session() as session:
                variables.initialize_local_variables()
                data_flow_ops.tables_initializer()
                resources.initialize_resources(resources.shared_resources())
                saver_for_restore.restore(session, checkpoint_path)
                init_op = control_flow_ops.group(
                    variables.local_variables_initializer(),
                    resources.initialize_resources(resources.shared_resources()),
                    data_flow_ops.tables_initializer())

                # Perform the export
                builder = saved_model_builder.SavedModelBuilder(export_dir)
                builder.add_meta_graph_and_variables(
                    session, [tag_constants.SERVING],
                    signature_def_map=signature_def_map,
                    assets_collection=ops.get_collection(ops.GraphKeys.ASSET_FILEPATHS),
                    legacy_init_op=init_op)
                builder.save(as_text)

            # Add the extra assets
            if assets_extra:
                assets_extra_path = os.path.join(compat.as_bytes(export_dir),
                                                 compat.as_bytes('assets.extra'))
                for dest_relative, source in assets_extra.items():
                    dest_absolute = os.path.join(compat.as_bytes(assets_extra_path),
                                                 compat.as_bytes(dest_relative))
                    dest_path = os.path.dirname(dest_absolute)
                    gfile.MakeDirs(dest_path)
                    gfile.Copy(source, dest_absolute)

            return export_dir

    @staticmethod
    def _check_hooks(hooks):
        """Returns hooks if all are SessionRunHook, raises TypeError otherwise."""
        hooks = list(hooks or [])
        for h in hooks:
            if not isinstance(h, SessionRunHook):
                raise TypeError("Hooks must be a SessionRunHook, given: {}".format(h))

        return hooks

    def train(self, input_fn=None, steps=None, hooks=None, max_steps=None):
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
        if (steps is not None) and (max_steps is not None):
            raise ValueError('Can not provide both steps and max_steps.')

        if max_steps is not None:
            try:
                start_step = load_variable(self._model_dir, ops.GraphKeys.GLOBAL_STEP)
                if max_steps <= start_step:
                    logging.info('Skipping training since max_steps has already saved.')
                    return self
            except:  # pylint: disable=bare-except
                pass

        hooks = self._check_hooks(hooks)
        if steps is not None or max_steps is not None:
            hooks.append(basic_session_run_hooks.StopAtStepHook(steps, max_steps))

        loss = self._train_model(input_fn=input_fn, hooks=hooks)
        logging.info('Loss for final step: %s.', loss)
        return self

    def evaluate(self, input_fn=None, steps=None, hooks=None, checkpoint_path=None, name=None):
        """Evaluates given model with provided evaluation data.

        Stop conditions - we evaluate on the given input data until one of the
        following:
        - If `steps` is provided, and `steps` batches of size `batch_size` are
        processed.
        - If `input_fn` is provided, and it raises an end-of-input
        exception (`OutOfRangeError` or `StopIteration`).
        - If `x` is provided, and all items in `x` have been processed.

        The return value is a dict containing the metrics specified in `metrics`, as
        well as an entry `global_step` which contains the value of the global step
        for which this evaluation was performed.

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
            name: Name of the evaluation if user needs to run multiple evaluations on
                different data sets, such as on training data vs test data.
            checkpoint_path: Path of a specific checkpoint to evaluate. If `None`,
                the latest checkpoint in `model_dir` is used.
            hooks: List of `SessionRunHook` subclass instances.
                Used for callbacks inside the evaluation call.

        Raises:
            ValueError: If `metrics` is not `None` or `dict`.

        Returns:
            Returns `dict` with evaluation results.
        """
        hooks = self._check_hooks(hooks)
        if steps is not None:
            if steps <= 0:
                raise ValueError('Must specify steps >= 0, given: {}'.format(steps))
            hooks.append(evaluation.StopAfterNEvalsHook(num_evals=steps))
        return self._evaluate_model(
            input_fn=input_fn, name=name, checkpoint_path=checkpoint_path, hooks=hooks)

    def predict(self, input_fn=None, predict_keys=None, hooks=None):
        """Returns predictions for given features.

        Args:
            input_fn: Input function.
            predict_keys: list of `str`, name of the output to predict. If `None`, returns all.
            hooks: List of `SessionRunHook` subclass instances.
                Used for callbacks inside the prediction call.

        Returns:
            A numpy array of predicted classes or regression values if the
            constructor's `model_fn` returns a `Tensor` for `predictions` or a `dict`
            of numpy arrays if `model_fn` returns a `dict`. Returns an iterable of
            predictions if as_iterable is True.

        """
        hooks = self._check_hooks(hooks)
        # Check that model has been trained.
        checkpoint_path = saver.latest_checkpoint(self._model_dir)
        if not checkpoint_path:
            raise NotFittedError("Couldn't find trained model at %s." % self._model_dir)

        with ops.Graph().as_default() as g:
            random_seed.set_random_seed(self._config.tf_random_seed)
            contrib_framework.create_global_step(g)
            features = self._get_features_from_input_fn(input_fn)
            estimator_spec = self._call_model_fn(features, None, model_fn_lib.ModeKeys.PREDICT)
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
                        for i in range(extract_batch_length(preds_evaluated)):
                            yield {key: value[i] for key, value in six.iteritems(preds_evaluated)}

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
    def _extract_metric_update_ops(eval_dict):
        """Separate update operations from metric value operations."""
        update_ops = []
        value_ops = {}
        for name, metric_ops in sorted(six.iteritems(eval_dict)):
            if isinstance(metric_ops, (list, tuple)):
                if len(metric_ops) == 2:
                    value_ops[name] = metric_ops[0]
                    update_ops.append(metric_ops[1])
                else:
                    logging.warning("Ignoring metric {}. It returned a list|tuple with len {}, "
                                    "expected 2".format(name, len(metric_ops)))
                    value_ops[name] = metric_ops
            else:
                value_ops[name] = metric_ops

        if update_ops:
            update_ops = control_flow_ops.group(*update_ops)
        else:
            update_ops = None

        return update_ops, value_ops

    @staticmethod
    def _get_features_from_input_fn(input_fn):
        result = input_fn()
        if isinstance(result, (list, tuple)):
            return result[0]
        return result

    @staticmethod
    def _extract_keys(predictions, predict_keys):
        if not predict_keys:
            return predictions
        if not isinstance(predictions, dict):
            raise ValueError("outputs argument is not valid in case of non-dict predictions.")
        existing_keys = predictions.keys()
        predictions = {
            key: value
            for key, value in six.iteritems(predictions) if key in predict_keys
        }
        if not predictions:
            raise ValueError("Expected to run at least one predict_keys from {}, "
                             "provided {}.".format(existing_keys, predict_keys))
        return predictions

    def _train_model(self, input_fn, hooks):
        all_hooks = []
        self._graph = ops.Graph()
        with self._graph.as_default() as g, g.device(self._device_fn):
            random_seed.set_random_seed(self._config.tf_random_seed)
            global_step = contrib_framework.create_global_step(g)
            features, labels = input_fn()
            estimator_spec = self._call_model_fn(features, labels, model_fn_lib.ModeKeys.TRAIN)
            # TODO check if need to track here ?
            ops.add_to_collection(ops.GraphKeys.LOSSES, estimator_spec.loss)
            all_hooks.extend([
                basic_session_run_hooks.NanTensorHook(estimator_spec.loss),
                basic_session_run_hooks.LoggingTensorHook(
                    {
                        'loss': estimator_spec.loss,
                        'step': global_step
                    },
                    every_n_iter=100)
            ])
            all_hooks.extend(hooks)
            all_hooks.extend(estimator_spec.training_hooks)

            scaffold = estimator_spec.scaffold or monitored_session.Scaffold()
            if not (scaffold.saver or ops.get_collection(ops.GraphKeys.SAVERS)):
                ops.add_to_collection(ops.GraphKeys.SAVERS,  # TODO remove non restorable vars
                                      saver.Saver(sharded=True,  # TODO `var_list`
                                                  max_to_keep=self._config.keep_checkpoint_max,
                                                  defer_build=True))

            chief_hooks = []
            if self._config.save_checkpoints_secs or self._config.save_checkpoints_steps:
                saver_hook_exists = any(
                    [isinstance(h, basic_session_run_hooks.CheckpointSaverHook)
                     for h in (all_hooks + estimator_spec.training_hooks +
                               chief_hooks + estimator_spec.training_chief_hooks)])
                if not saver_hook_exists:
                    chief_hooks = [
                        basic_session_run_hooks.CheckpointSaverHook(
                            self._model_dir,
                            save_secs=self._config.save_checkpoints_secs,
                            save_steps=self._config.save_checkpoints_steps,
                            scaffold=scaffold)
                    ]
            with monitored_session.MonitoredTrainingSession(
                    master=self._config.master,
                    is_chief=self._config.is_chief,
                    checkpoint_dir=self._model_dir,
                    scaffold=scaffold,
                    hooks=all_hooks + estimator_spec.training_hooks,
                    chief_only_hooks=chief_hooks + estimator_spec.training_chief_hooks,
                    save_checkpoint_secs=0,  # Saving is handled by a hook.
                    save_summaries_steps=self._config.save_summary_steps,
                    config=self._session_config) as mon_sess:
                loss = None
                while not mon_sess.should_stop():
                    _, loss = mon_sess.run([estimator_spec.train_op, estimator_spec.loss])
            summary_io.SummaryWriterCache.clear()
            return loss

    def _evaluate_model(self, input_fn, hooks=None, checkpoint_path=None, name=''):
        # Check that model has been trained (if nothing has been set explicitly).
        if not checkpoint_path:
            latest_path = saver.latest_checkpoint(self._model_dir)
            if not latest_path:
                raise NotFittedError("Couldn't find trained model at {}.".format(self._model_dir))
            checkpoint_path = latest_path

        # Setup output directory.
        eval_dir = os.path.join(self._model_dir, 'eval' if not name else 'eval_' + name)

        with ops.Graph().as_default() as g:
            random_seed.set_random_seed(self._config.tf_random_seed)
            global_step = contrib_framework.create_global_step(g)
            features, labels = input_fn()

            estimator_spec = self._call_model_fn(features, labels, model_fn_lib.ModeKeys.EVAL)
            if model_fn_lib.MetricKeys.LOSS in estimator_spec.eval_metric_ops:
                raise ValueError("Metric with name `{}` is not allowed, because Estimator "
                                 "already defines a default metric "
                                 "with the same name.".format(model_fn_lib.MetricKeys.LOSS))
            estimator_spec.eval_metric_ops[
                model_fn_lib.MetricKeys.LOSS] = metrics_lib.streaming_mean(estimator_spec.loss)
            update_op, eval_dict = self._extract_metric_update_ops(estimator_spec.eval_metric_ops)

            if ops.GraphKeys.GLOBAL_STEP in eval_dict:
                raise ValueError("Metric with name `global_step` is not allowed, because "
                                 "Estimator already defines a default metric with the same name.")
            eval_dict[ops.GraphKeys.GLOBAL_STEP] = global_step

            eval_results = evaluation.evaluate_once(
                checkpoint_path=checkpoint_path,
                master=self._config.evaluation_master,
                scaffold=estimator_spec.scaffold,
                eval_ops=update_op,
                final_ops=eval_dict,
                hooks=hooks,
                config=self._session_config)

            self._write_dict_to_summary(
                output_dir=eval_dir,
                dictionary=eval_results,
                current_global_step=eval_results[ops.GraphKeys.GLOBAL_STEP])

            return eval_results

    @staticmethod
    def _write_dict_to_summary(output_dir,
                               dictionary,
                               current_global_step):
        """Writes a `dict` into summary file in given output directory.

          Args:
            output_dir: `str`, directory to write the summary file in.
            dictionary: the `dict` to be written to summary file.
            current_global_step: `int`, the current global step.
          """
        logging.info('Saving dict for global step %d: %s', current_global_step,
                     dict_to_str(dictionary))
        summary_writer = summary_io.SummaryWriterCache.get(output_dir)
        summary_proto = summary_pb2.Summary()
        for key in dictionary:
            if dictionary[key] is None:
                continue
            value = summary_proto.value.add()
            value.tag = key
            if (isinstance(dictionary[key], np.float32) or
                    isinstance(dictionary[key], float)):
                value.simple_value = float(dictionary[key])
            else:
                logging.warn('Skipping summary for %s, must be a float or np.float32.', key)
        summary_writer.add_summary(summary_proto, current_global_step)
        summary_writer.flush()


ESTIMATORS = {
    'estimator': Estimator
}

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow.contrib.framework import list_variables, load_variable
from tensorflow.python.framework import ops, random_seed
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import (
    evaluation,
    monitored_session,
    saver,
    summary_io,
    training
)

from polyaxon import Modes
from polyaxon.estimators import Estimator
from polyaxon.estimators import hooks as plx_hooks
from polyaxon.rl.environments import Environment
from polyaxon.rl.utils import get_or_create_global_episode, get_or_create_global_timestep


class Agent(Estimator):
    """Agent class is the basic reinforcement learning model trainer/evaluator.

    Constructs an `Agent` instance.

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
    def __init__(self, model_fn, memory_config, model_dir=None, config=None, params=None):
        super(Agent, self).__init__(
            model_fn=model_fn, model_dir=model_dir, config=config, params=params)
        self.memory_config = memory_config

    def _prepare_train(self, first_update=1, update_frequency=1, episodes=None, steps=None,
                       hooks=None, max_steps=None, max_episodes=None):
        if first_update < 0:
            raise ValueError("Must specify first_update > 0, given: {}".format(first_update))
        if update_frequency < 0:
            raise ValueError(
                "Must specify update_frequency > 0, given: {}".format(update_frequency))
        hooks = super(Agent, self)._prepare_train(steps=steps, hooks=hooks, max_steps=max_steps)

        if max_episodes is not None:
            try:
                start_episode = load_variable(self._model_dir, ops.GraphKeys.GLOBAL_EPISODE)
                if max_episodes <= start_episode:
                    logging.info('Skipping training since max_episode has already saved.')
                    return self
            except:  # pylint: disable=bare-except
                pass

        hooks = self._check_hooks(hooks)
        if steps is not None or max_steps is not None:
            hooks.append(plx_hooks.StopAtEpisodeHook(episodes, max_episodes))

        return hooks

    def train(self, env, first_update=2, update_frequency=1, episodes=None, steps=None, hooks=None,
              max_steps=None, max_episodes=None):
        """Trains a model given an environment.

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

            Two calls to `fit(steps=100)` means 200 training iterations.
            On the other hand, two calls to `fit(max_steps=100)` means
            that the second call will not do any iteration since first call did all 100 steps.

        Returns:
            `self`, for chaining.
        """
        hooks = self._prepare_train(
            first_update, update_frequency, steps, hooks, max_steps, max_episodes)
        loss = self._train_model(env=env, first_update=first_update,
                                 update_frequency=update_frequency, hooks=hooks)
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
            hooks.append(evaluation._StopAfterNEvalsHook(num_evals=steps))
        return self._evaluate_model(
            input_fn=input_fn, name=name, checkpoint_path=checkpoint_path, hooks=hooks)

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
        return self._infer(Modes.PREDICT, input_fn=input_fn, predict_keys=predict_keys, hooks=hooks,
                           checkpoint_path=checkpoint_path)

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
    def _get_features_from_input_fn(input_fn):
        result = input_fn()
        if not ops.get_default_graph().get_collection(ops.GraphKeys.QUEUE_RUNNERS):
            logging.warning('Input graph does not contain a QueueRunner. '
                            'That means predict yields forever. '
                            'This is probably a mistake.')
        if isinstance(result, (list, tuple)):
            return result[0]
        return result

    def _prepare_input_fn(self, mode, env):
        """Creates placeholders for the model given the mode and the env.

        Args:
            mode: Specifies if this training, evaluation or prediction. See `Modes`.

        Returns:
            `tuple`: (features, labels).
                    features: `dict`. {state: array}
                    labels: `dict`. {action: array, reward: array, done: array}
        """
        if not isinstance(env, Environment):
            raise TypeError("`env` must be an instance of `Environment`, "
                            "got `{}`".format(type(env)))

        features = {'state': tf.placeholder(
            dtype=tf.float32, shape=[None, env.num_states], name='state')}

        if Modes.is_train(mode) or Modes.is_eval(mode):
            return (
                features,
                {
                    'action': tf.placeholder(
                        dtype=tf.float32 if env.is_continuous else tf.int64,
                        shape=[None, env.num_actions] if env.is_continuous else [None, ],
                        name='action'),
                    'reward': tf.placeholder(dtype=tf.float32, shape=(None,), name='reward'),
                    'done': tf.placeholder(dtype=tf.bool, shape=(None,), name='done'),
                }
            )
        if Modes.is_infer(mode):
            return features, None

    def _prepare_feed_dict(self, mode, features, labels, env_spec):
        feed_dict = {features['state']: [env_spec.next_state]}
        if mode == 'observe':
            feed_dict = {
                    features['state']: [env_spec.state],
                    labels['action']: [env_spec.action],
                    labels['reward']: [env_spec.reward],
                    labels['done']: [env_spec.done],
                }
        return feed_dict

    def run_episode(self, env, sess, features, labels, no_run_hooks, global_step,
                    update_episode_op, update_timestep_op, first_update, update_frequency,
                    estimator_spec):
        """We need to differentiate between the `global_timestep` and `global_step`.

         The `global_step` gets updated directly by the `train_op` and has an effect
         on the training learning rate, especially if it gets decayed.

         The `global_timestep` on the other hand is related to the episode and how many times
         our agent acted. It has an effect on the exploration rate and how it's annealed.

        Args:
            env: `Environment` instance.
            sess: `MonitoredTrainingSession` instance.
            first_update: The first timestep we should invoke the train_op and update
                the model loss.
            update_frequency: The frequency of calculating the loss of the model.
            estimator_spec: `EstimatorSpec` instance.

        Returns:
            statistics about episode.
        """
        env_spec = env.reset()
        loss = None
        episode_done = False
        while not env_spec.done:
            _, step, timestep, action = sess.run(
                [no_run_hooks, global_step, update_timestep_op, estimator_spec.predictions['results']],
                feed_dict=self._prepare_feed_dict('act', features, labels, env_spec))
            env_spec = env.step(action, env_spec.next_state)
            if env_spec.done:  # TODO: max timestep by episode should also update the episode
                #  Increment episode number to trigger EpisodeHooks (logging, summary, checkpoint)
                episode_done = True
                sess.run([no_run_hooks, update_episode_op])
            if (timestep > first_update and timestep % update_frequency == 0) or episode_done:
                _, loss = sess.run(
                    [estimator_spec.train_op, estimator_spec.loss],
                    feed_dict=self._prepare_feed_dict('observe', features, labels, env_spec))
        return loss

    def _train_model(self, env, first_update, update_frequency, hooks):
        all_hooks = []
        self._graph = ops.Graph()
        with self._graph.as_default() as g, g.device(self._device_fn):
            random_seed.set_random_seed(self._config.tf_random_seed)
            global_step = training.get_or_create_global_step(g)
            global_episode = get_or_create_global_episode(g)
            global_timestep = get_or_create_global_timestep(g)
            update_episode_op = tf.assign_add(global_episode, 1)
            update_timestep_op = tf.assign_add(global_timestep, 1)
            no_run_hooks = tf.no_op(name='no_run_hooks')
            with ops.device('/cpu:0'):
                features, labels = self._prepare_input_fn(Modes.TRAIN, env)
            estimator_spec = self._call_model_fn(features, labels, Modes.TRAIN)
            ops.add_to_collection(ops.GraphKeys.LOSSES, estimator_spec.loss)
            all_hooks.extend([
                plx_hooks.NanTensorHook(estimator_spec.loss),
                plx_hooks.StepLoggingTensorHook(
                    {
                        'loss': estimator_spec.loss,
                        'step': global_step,
                        'timestep': global_timestep,
                        'global_episode': global_episode
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

            chief_hooks = [
                plx_hooks.EpisodeLoggingTensorHook(
                    {
                        'loss': estimator_spec.loss,
                        'step': global_step,
                        'global_timestep': global_timestep,
                        'global_episode': global_episode
                    },
                    every_n_episodes=1)  # TODO: save every episode?
            ]
            if self._config.save_checkpoints_secs or self._config.save_checkpoints_steps:
                saver_hook_exists = any(
                    [isinstance(h, plx_hooks.EpisodeCheckpointSaverHook)
                     for h in (all_hooks +
                               chief_hooks +
                               list(estimator_spec.training_chief_hooks))])
                if not saver_hook_exists:
                    chief_hooks += [
                        plx_hooks.EpisodeCheckpointSaverHook(
                            self._model_dir,
                            save_episodes=1,  # TODO: save every episode?
                            scaffold=scaffold)
                    ]
            if self._config.save_summary_steps:
                saver_hook_exists = any(
                    [isinstance(h, plx_hooks.EpisodeSummarySaverHook)
                     for h in (all_hooks +
                               chief_hooks +
                               list(estimator_spec.training_chief_hooks))])
                if not saver_hook_exists:
                    chief_hooks += [
                        plx_hooks.EpisodeSummarySaverHook(
                            scaffold=scaffold,
                            save_episodes=1,  # TODO: save every episode?
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
                    loss = self.run_episode(
                        env=env, sess=mon_sess, features=features, labels=labels,
                        no_run_hooks=no_run_hooks, global_step=global_step,
                        update_episode_op=update_episode_op, update_timestep_op=update_timestep_op,
                        first_update=first_update, update_frequency=update_frequency,
                        estimator_spec=estimator_spec)
            summary_io.SummaryWriterCache.clear()
            return loss

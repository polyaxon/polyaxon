# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import time
from collections import OrderedDict

import numpy as np
import tensorflow as tf
from tensorflow.core.util.event_pb2 import SessionLog
from tensorflow.core.framework.summary_pb2 import Summary
from tensorflow.python.framework import meta_graph
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.training import basic_session_run_hooks, session_run_hook
from tensorflow.python.training import training_util
from tensorflow.python.training.summary_io import SummaryWriterCache

from polyaxon.estimators.hooks.utils import can_run_hook
from polyaxon.libs.utils import get_tracked
from polyaxon.rl.utils import get_global_episode


class EpisodeTimer(object):
    """Timer that triggers at most once every N episodes."""
    def __init__(self, every_episodes):
        self._every_episodes = every_episodes
        self._last_triggered_episode = None
        self._last_triggered_time = None

    def should_trigger_for_episode(self, episode):
        """Return true if the timer should trigger for the specified step.

        Args:
          episode: Training episode to trigger on.

        Returns:
          True if the difference between the current episode and the last triggered episode exceeds
          `every_episodes`. False otherwise.
        """
        if self._last_triggered_episode is None:
            return True

        if self._last_triggered_episode == episode:
            return False

        if self._every_episodes is not None:
            if episode >= self._last_triggered_episode + self._every_episodes:
                return True

        return False

    def update_last_triggered_episode(self, episode):
        """Update the last triggered time and episode number.

        Args:
          episode: The current episode.

        Returns:
          A pair `(elapsed_time, elapsed_episodes)`, where `elapsed_time` is the number
          of seconds between the current trigger and the last one (a float), and
          `elapsed_episodes` is the number of episodes between the current trigger and
          the last one. Both values will be set to `None` on the first trigger.
        """
        current_time = time.time()
        if self._last_triggered_time is None:
            elapsed_secs = None
            elapsed_episodes = None
        else:
            elapsed_secs = current_time - self._last_triggered_time
            elapsed_episodes = episode - self._last_triggered_episode

        self._last_triggered_time = current_time
        self._last_triggered_episode = episode
        return elapsed_secs, elapsed_episodes

    def last_triggered_episode(self):
        return self._last_triggered_episode


class StopAtEpisodeHook(session_run_hook.SessionRunHook):
    """Monitor to request stop at a specified episode."""

    def __init__(self, num_episodes=None, last_episode=None):
        """Create a StopAtStep Hook.

        This hook requests stop after either a number of episodes have been
        executed or a last episode has been reached. Only one of the two options can be
        specified.

        if `num_episode` is specified, it indicates the number of episodes to execute
        after `begin()` is called. If instead `last_episode` is specified, it
        indicates the last episode we want to execute, as passed to the `after_run()`
        call.

        Args:
            num_episodes: Number of episodes to execute.
            last_episode: Step after which to stop.

        Raises:
            ValueError: If one of the arguments is invalid.
        """
        if num_episodes is None and last_episode is None:
            raise ValueError("One of num_episodes or last_episode must be specified.")
        if num_episodes is not None and last_episode is not None:
            raise ValueError("Only one of num_episodes or last_episode can be specified.")
        self._num_episodes = num_episodes
        self._last_episode = last_episode
        self._global_episode_tensor = None

    def begin(self):
        self._global_episode_tensor = get_global_episode()
        if self._global_episode_tensor is None:
            raise RuntimeError("Global episode should be created to use StopAtEpisodeHook.")

    def before_run(self, run_context):  # pylint: disable=unused-argument
        return session_run_hook.SessionRunArgs(self._global_episode_tensor)

    def after_run(self, run_context, run_values):
        global_episode = run_values.results
        if self._last_episode is None:
            self._last_episode = global_episode + self._num_episodes - 1
        if global_episode >= self._last_episode:
            run_context.request_stop()


class EpisodeLoggingTensorHook(session_run_hook.SessionRunHook):
    def __init__(self, tensors, every_n_episodes, formatter=None):
        """Initializes an EpisodeLoggingHook monitor.

        This Hook should be used with Agents and requires a `global_episode`.

        Args:
          tensors: `dict` that maps string-valued tags to tensors/tensor names,
              or `iterable` of tensors/tensor names.
          every_n_episodes: `int`, print the values of `tensors` once every N local
              episodes taken on the current worker.
          formatter: function, takes dict of `tag`->`Tensor` and returns a string.
              If `None` uses default printing all tensors.

        Raises:
          ValueError: if `every_n_iter` is non-positive.
        """
        if every_n_episodes is not None and every_n_episodes <= 0:
            raise ValueError("invalid every_n_episodes={}.".format(every_n_episodes))
        if not isinstance(tensors, dict):
            self._tag_order = tensors
            tensors = {item: item for item in tensors}
        else:
            self._tag_order = tensors.keys()
        self._tensors = tensors
        self._formatter = formatter
        self._timer = EpisodeTimer(every_episodes=every_n_episodes)

    def begin(self):
        self._global_episode_tensor = get_global_episode()
        if self._global_episode_tensor is None:
            raise RuntimeError("Global episode should be created to use StopAtEpisodeHook.")

        # Convert names to tensors if given
        self._current_tensors = {tag: basic_session_run_hooks._as_graph_element(tensor)
                                 for (tag, tensor) in self._tensors.items()}
        self._current_tensors['global_episode'] = self._global_episode_tensor

    def before_run(self, run_context):  # pylint: disable=unused-argument
        if can_run_hook(run_context):
            return session_run_hook.SessionRunArgs(self._current_tensors)
        else:
            return session_run_hook.SessionRunArgs({'global_episode': self._global_episode_tensor})

    def after_run(self, run_context, run_values):
        global_episode = run_values.results['global_episode']
        if can_run_hook(run_context):
            if self._timer.should_trigger_for_episode(global_episode):
                original = np.get_printoptions()
                np.set_printoptions(suppress=True)
                elapsed_secs, _ = self._timer.update_last_triggered_episode(global_episode)
                if self._formatter:
                    logging.info(self._formatter(run_values.results))
                else:
                    stats = []
                    for tag in self._tag_order:
                        stats.append("%s = %s" % (tag, run_values.results[tag]))
                    if elapsed_secs is not None:
                        logging.info("%s (%.3f sec)", ", ".join(stats), elapsed_secs)
                    else:
                        logging.info("%s", ", ".join(stats))
                np.set_printoptions(**original)


class EpisodeSummarySaverHook(basic_session_run_hooks.SummarySaverHook):
    """Saves summaries every N episode.

    Args:
        save_episodes: `int`, save summaries every N episodes. Exactly one of
            `save_secs` and `save_episodes` should be set.
        output_dir: `string`, the directory to save the summaries to. Only used
            if no `summary_writer` is supplied.
        summary_writer: `SummaryWriter`. If `None` and an `output_dir` was passed,
            one will be created accordingly.
        scaffold: `Scaffold` to get summary_op if it's not provided.
        summary_op: `Tensor` of type `string` containing the serialized `Summary`
            protocol buffer or a list of `Tensor`. They are most likely an output
            by TF summary methods like `tf.summary.scalar` or
            `tf.summary.merge_all`. It can be passed in as one tensor; if more
            than one, they must be passed in as a list.

    Raises:
        ValueError: Exactly one of scaffold or summary_op should be set.
    """
    def __init__(self, save_episodes=None, output_dir=None, summary_writer=None, scaffold=None,
                 summary_op=None):
        if output_dir is None:
            raise ValueError("`output_dir` must be provided")
        if ((scaffold is None and summary_op is None) or
                (scaffold is not None and summary_op is not None)):
            raise ValueError(
                "Exactly one of scaffold or summary_op must be provided.")
        self._summary_op = summary_op
        self._summary_writer = summary_writer
        self._output_dir = output_dir
        self._scaffold = scaffold
        self._request_summary = False
        self._timer = EpisodeTimer(every_episodes=save_episodes)

    def begin(self):
        if self._summary_writer is None and self._output_dir:
            self._summary_writer = SummaryWriterCache.get(self._output_dir)
        self._next_episode = None
        self._current_episode = None
        self._global_episode_tensor = get_global_episode()
        if self._global_episode_tensor is None:
            raise RuntimeError("Global episode should be created to use EpisodeSummarySaverHook.")

    def before_run(self, run_context):  # pylint: disable=unused-argument
        requests = {"global_episode": self._global_episode_tensor}
        if can_run_hook(run_context):
            self._request_summary = self._current_episode == self._next_episode
            if self._request_summary:
                if self._get_summary_op() is not None:
                    requests["summary"] = self._get_summary_op()

        return basic_session_run_hooks.SessionRunArgs(requests)

    def after_run(self, run_context, run_values):
        _ = run_context
        if not self._summary_writer:
            return

        global_episode = run_values.results["global_episode"]

        if self._next_episode is None:
            self._next_episode = global_episode + 1
            self._summary_writer.add_session_log(SessionLog(status=SessionLog.START), global_episode)

        if self._request_summary and self._timer.should_trigger_for_episode(global_episode):
            self._timer.update_last_triggered_episode(global_episode)
            self._next_episode = global_episode + 1
            if "summary" in run_values.results:
                for summary in run_values.results["summary"]:
                    self._summary_writer.add_summary(summary, global_episode)

        self._current_episode = global_episode

    def end(self, session=None):
        if self._summary_writer:
            self._summary_writer.flush()

    def _get_summary_op(self):
        """Fetches the summary op either from self._summary_op or tf.GraphKeys.EPISODE_SUMMARIES.

        Returns:
          Returns a list of summary `Tensor`.
        """
        if self._summary_op is not None:
            summary_op = self._summary_op
        elif self._scaffold.summary_op is not None:
            summary_op = self._scaffold.summary_op
        else:
            summary_op = get_tracked(tf.GraphKeys.EPISODE_SUMMARIES)

        if summary_op is None:
            return None

        if not isinstance(summary_op, list):
            return [summary_op]
        return summary_op


class EpisodeCheckpointSaverHook(session_run_hook.SessionRunHook):
    """Saves checkpoints every N episodes.
    Args:
        checkpoint_dir: `str`, base directory for the checkpoint files.
        save_episodes: `int`, save every N episodes.
        saver: `Saver` object, used for saving.
        checkpoint_basename: `str`, base name for the checkpoint files.
        scaffold: `Scaffold`, use to get saver object.
        listeners: List of `CheckpointSaverListener` subclass instances.
            Used for callbacks that run immediately after the corresponding
            CheckpointSaverHook callbacks, only in episodes where the
            CheckpointSaverHook was triggered.

    Raises:
        ValueError: One of `save_episodes` or `save_secs` should be set.
        ValueError: Exactly one of saver or scaffold should be set.
    """
    def __init__(self, checkpoint_dir, save_episodes=None, saver=None,
                 checkpoint_basename="model.ckpt", scaffold=None, listeners=None):
        logging.info("Create CheckpointSaverHook.")
        if ((saver is None and scaffold is None) or
                (saver is not None and scaffold is not None)):
            raise ValueError("Exactly one of saver or scaffold must be provided.")
        self._saver = saver
        self._checkpoint_dir = checkpoint_dir
        self._save_path = os.path.join(checkpoint_dir, checkpoint_basename)
        self._scaffold = scaffold
        self._timer = EpisodeTimer(every_episodes=save_episodes)
        self._listeners = listeners or []

    def begin(self):
        self._summary_writer = SummaryWriterCache.get(self._checkpoint_dir)
        self._global_episode_tensor = get_global_episode()
        if self._global_episode_tensor is None:
            raise RuntimeError(
                "Global step should be created to use CheckpointSaverHook.")
        for l in self._listeners:
            l.begin()

    def before_run(self, run_context):  # pylint: disable=unused-argument
        if can_run_hook(run_context) and self._timer.last_triggered_episode() is None:
            # We do write graph and saver_def at the first call of before_run.
            # We cannot do this in begin, since we let other hooks to change graph and
            # add variables in begin. Graph is finalized after all begin calls.
            training_util.write_graph(
                tf.get_default_graph().as_graph_def(add_shapes=True),
                self._checkpoint_dir,
                "graph.pbtxt")
            saver_def = self._get_saver().saver_def if self._get_saver() else None
            graph = tf.get_default_graph()
            meta_graph_def = meta_graph.create_meta_graph_def(
                graph_def=graph.as_graph_def(add_shapes=True),
                saver_def=saver_def)
            self._summary_writer.add_graph(graph)
            self._summary_writer.add_meta_graph(meta_graph_def)

        return basic_session_run_hooks.SessionRunArgs(self._global_episode_tensor)

    def after_run(self, run_context, run_values):
        global_episode = run_values.results
        if can_run_hook(run_context) and self._timer.should_trigger_for_episode(global_episode):
            self._timer.update_last_triggered_episode(global_episode)
            self._save(global_episode, run_context.session)

    def end(self, session):
        last_episode = session.run(get_global_episode())
        if last_episode != self._timer.last_triggered_episode():
            self._save(last_episode, session)
        for l in self._listeners:
            l.end(session, last_episode)

    def _save(self, episode, session):
        """Saves the latest checkpoint."""
        logging.info("Saving checkpoints for episode {} into {}.".format(episode, self._save_path))

        for l in self._listeners:
            l.before_save(session, episode)

        self._get_saver().save(session, self._save_path, global_step=episode)
        self._summary_writer.add_session_log(
            SessionLog(status=SessionLog.CHECKPOINT, checkpoint_path=self._save_path), episode)

        for l in self._listeners:
            l.after_save(session, episode)

    def _get_saver(self):
        if self._saver is not None:
            return self._saver
        elif self._scaffold is not None:
            return self._scaffold.saver
        return None


class EpisodeCounterHook(session_run_hook.SessionRunHook):
    """TimeSteps and Seconds per episode."""
    def __init__(self, output_dir=None, summary_writer=None):
        self._timer = EpisodeTimer(every_episodes=1)
        self._summary_writer = summary_writer
        self._output_dir = output_dir

    def begin(self):
        if self._summary_writer is None and self._output_dir:
            self._summary_writer = SummaryWriterCache.get(self._output_dir)
        self._global_episode_tensor = get_global_episode()
        if self._global_episode_tensor is None:
            raise RuntimeError("Global step should be created to use EpisodeCounterHook.")
        self._summary_sec_tag = self._global_episode_tensor.op.name + "/sec"
        self._summary_steps_tag = self._global_episode_tensor.op.name + "/steps"
        self._num_steps = 0

    def before_run(self, run_context):  # pylint: disable=unused-argument
        return session_run_hook.SessionRunArgs(self._global_episode_tensor)

    def after_run(self, run_context, run_values):
        global_episode = run_values.results
        self._num_steps += 1
        if self._timer.should_trigger_for_episode(global_episode):
            elapsed_time, elapsed_steps = self._timer.update_last_triggered_episode(global_episode)
            if elapsed_time is not None:
                steps_per_sec = elapsed_steps / elapsed_time
                if self._summary_writer is not None:
                    summary = Summary(value=[
                        Summary.Value(tag=self._summary_sec_tag, simple_value=steps_per_sec),
                        Summary.Value(tag=self._summary_steps_tag, simple_value=self._num_steps),
                    ])
                    self._summary_writer.add_summary(summary, global_episode)
                logging.info("%s: %g, %s: %d",
                             self._summary_sec_tag, steps_per_sec,
                             self._summary_steps_tag, self._num_steps)
                self._num_steps = 0


EPISODE_HOOKS = OrderedDict([
    ('EpisodeLoggingTensorHook', EpisodeLoggingTensorHook),
    ('StopAtEpisodeHook', StopAtEpisodeHook),
    ('EpisodeSummarySaverHook', EpisodeSummarySaverHook),
    ('EpisodeCounterHook', EpisodeCounterHook),
])

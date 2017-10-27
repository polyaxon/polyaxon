<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/episode_hooks.py#L126)</span>
## EpisodeLoggingTensorHook

```python
polyaxon.estimators.hooks.episode_hooks.EpisodeLoggingTensorHook(tensors, every_n_episodes, formatter=None)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/episode_hooks.py#L80)</span>
## StopAtEpisodeHook

```python
polyaxon.estimators.hooks.episode_hooks.StopAtEpisodeHook(num_episodes=None, last_episode=None)
```

Monitor to request stop at a specified episode.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/episode_hooks.py#L191)</span>
## EpisodeSummarySaverHook

```python
polyaxon.estimators.hooks.episode_hooks.EpisodeSummarySaverHook(save_episodes=None, output_dir=None, summary_writer=None, scaffold=None, summary_op=None)
```

Saves summaries every N episode.

- __Args__:
	- __save_episodes__: `int`, save summaries every N episodes. Exactly one of
		`save_secs` and `save_episodes` should be set.
	- __output_dir__: `string`, the directory to save the summaries to. Only used
		if no `summary_writer` is supplied.
	- __summary_writer__: `SummaryWriter`. If `None` and an `output_dir` was passed,
		one will be created accordingly.
	- __scaffold__: `Scaffold` to get summary_op if it's not provided.
	- __summary_op__: `Tensor` of type `string` containing the serialized `Summary`
		protocol buffer or a list of `Tensor`. They are most likely an output
		by TF summary methods like `tf.summary.scalar` or
		`tf.summary.merge_all`. It can be passed in as one tensor; if more
		than one, they must be passed in as a list.

- __Raises__:
	- __ValueError__: Exactly one of scaffold or summary_op should be set.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/estimators/hooks/episode_hooks.py#L386)</span>
## EpisodeCounterHook

```python
polyaxon.estimators.hooks.episode_hooks.EpisodeCounterHook(output_dir=None, summary_writer=None)
```

TimeSteps and Seconds per episode.
<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L114)</span>
## PipelineConfig

```python
polyaxon.libs.configs.PipelineConfig(module=None, name=None, subgraph_configs_by_features=None, dynamic_pad=True, bucket_boundaries=False, batch_size=64, num_epochs=4, min_after_dequeue=5000, num_threads=3, shuffle=False, allow_smaller_final_batch=True, params=None)
```

The PipelineConfig holds information needed to create a `Pipeline`.

- __Args__:
	- __module__: `str`, the pipeline module to use.
	- __name__: `str`, name to give for the pipeline.
	- __dynamic_pad__: `bool`, If True the piple uses dynamic padding.
	- __bucket_boundaries__:
	- __batch_size__: `int`, the batch size.
	- __num_epochs__: number of epochs to iterate over in this pipeline.
	- __min_after_dequeue__: `int`, number of element to have in the queue.
	- __num_threads__: `int`, number of threads to use in the queue.
	- __shuffle__: If true, shuffle the data.
	- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.
	- __params__: `dict`, extra information to pass to the pipeline.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L20)</span>
## RunConfig

```python
polyaxon.libs.configs.RunConfig(master=None, num_cores=0, log_device_placement=False, gpu_memory_fraction=1.0, tf_random_seed=None, save_summary_steps=100, save_checkpoints_secs=600, save_checkpoints_steps=None, keep_checkpoint_max=5, keep_checkpoint_every_n_hours=10000, evaluation_master='', model_dir=None)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L67)</span>
## Configurable

```python
polyaxon.libs.configs.Configurable()
```

`Configurable` is an abstract class for defining an configurable objects.

A configurable class reads a configuration (YAML, Json) and create a config instance.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L359)</span>
## EstimatorConfig

```python
polyaxon.libs.configs.EstimatorConfig(module='Estimator', output_dir=None, params=None)
```

The EstimatorConfig holds information needed to create a `Estimator`.

- __Args__:
	- __cls__: `str`, estimator class to use.
	- __output_dir__: `str`, where to save training and evaluation data.
	- __params__: `dict`, extra information to pass to the estimator.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L165)</span>
## InputDataConfig

```python
polyaxon.libs.configs.InputDataConfig(input_type=None, pipeline_config=None, x=None, y=None)
```

The InputDataConfig holds information needed to create a `InputData`.

- __Args__:
	- __input_type__: `str`, the type of the input data, e.g. numpy arrays.
	- __pipeline_config__: The pipeline config to use.
	- __x__: The x values, only used with NUMPY and PANDAS types.
	- __y__: The y values, only used with NUMPY and PANDAS types.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L192)</span>
## LossConfig

```python
polyaxon.libs.configs.LossConfig(module, params=None)
```

The LossConfig holds information needed to create a `Loss`.

- __Args__:
	- __module__: `str`, module loss to use.
	- __params__: `dict`, extra information to pass to the loss.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L204)</span>
## MetricConfig

```python
polyaxon.libs.configs.MetricConfig(module, params=None)
```

The MetricConfig holds information needed to create a `Metric`.

- __Args__:
	- __module__: `str`, name to give for the metric.
	- __params__: `dict`, extra information to pass to the metric.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L216)</span>
## OptimizerConfig

```python
polyaxon.libs.configs.OptimizerConfig(module, learning_rate=0.0001, decay_type='', decay_steps=100, decay_rate=0.99, start_decay_at=0, stop_decay_at=2147483647, min_learning_rate=1e-12, staircase=False, sync_replicas=0, sync_replicas_to_aggregate=0, params=None)
```

The OptimizerConfig holds information needed to create a `Optimizer`.

- __Args__:
	- __module__: `str`, optimizer optimizer to use.
	- __learning_rate__: A Tensor or a floating point value. The learning rate to use.
	- __decay_steps__: How often to apply decay.
	- __decay_rate__: A Python number. The decay rate.
	- __start_decay_at__: Don't decay before this step
	- __stop_decay_at__: Don't decay after this step
	- __min_learning_rate__: Don't decay below this number
	- __decay_type__: A decay function name defined in `tf.train`
		possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
				 piecewise_constant, polynomial_decay.
	- __staircase__: Whether to apply decay in a discrete staircase,
		as opposed to continuous, fashion.
	- __sync_replicas__:
	- __sync_replicas_to_aggregate__:
	- __params__: `dict`, extra information to pass to the optimizer.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L254)</span>
## SubGraphConfig

```python
polyaxon.libs.configs.SubGraphConfig(modules, kwargs, features=None, module=None)
```

The configuration used to create subgraphs.

Handles also nested subgraphs.

- __Args__:
	- __name__: `str`. The name of this subgraph, used for creating the scope.
	- __modules__: `list`.  The modules to connect inside this subgraph, e.g. layers
	- __features__: `list`. The list of features to use for this subgraph.
	- __module__: `str`. The Subgraph module to use. e.g.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L298)</span>
## BridgeConfig

```python
polyaxon.libs.configs.BridgeConfig(module, state_size=None)
```

The BridgeConfig class holds information neede to create a `Bridge` for a generator model.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L308)</span>
## ModelConfig

```python
polyaxon.libs.configs.ModelConfig(loss_config, optimizer_config, module=None, graph_config=None, encoder_config=None, decoder_config=None, bridge_config=None, summaries='all', eval_metrics_config=None, clip_gradients=5.0, clip_embed_gradients=0.1)
```

The ModelConfig holds information needed to create a `Model`.

- __Args__:
	- __loss_config__: The loss configuration.
	- __optimizer_config__: The optimizer configuration.
	- __graph_config__: The graph configuration.
	- __model_type__: `str`, The type of the model (`classifier`, 'regressor, or `generator`).
	- __summaries__: `str` or `list`, the summary levels.
	- __eval_metrics_config__: The evaluation metrics configuration.
	- __clip_gradients__: `float`, The value to clip the gradients with.
	- __params__: `dict`, extra information to pass to the model.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/configs.py#L389)</span>
## ExperimentConfig

```python
polyaxon.libs.configs.ExperimentConfig(name, output_dir, run_config, train_input_data_config, eval_input_data_config, estimator_config, model_config, train_hooks_config=None, eval_hooks_config=None, eval_metrics_config=None, eval_every_n_steps=1000, train_steps=10000, eval_steps=10, eval_delay_secs=0, continuous_eval_throttle_secs=60, delay_workers_by_global_step=False, export_strategies=None, train_steps_per_iteration=1000)
```

The ExperimentConfig holds information needed to create a `Experiment`.

- __Args__:
	- __name__: `str`, name to give for the experiment.
	- __output_dir__: `str`, where to save training and evaluation data.
	- __run_config__: Tensorflow run config.
	- __train_input_data_config__: Train input data configuration.
	- __eval_input_data_config__: Eval input data configuration.
	- __estimator_config__: The estimator configuration.
	- __model_config__: The model configuration.
	- __train_hooks_config__: The training hooks configuration.
	- __eval_hooks_config__: The evaluation hooks configuration.
	- __eval_metrics_config__: The evaluation metrics config.
	- __eval_every_n_steps__: `int`, the frequency of evaluation.
	- __train_steps__: `int`, the number of steps to train the model.
	- __eval_steps__: `int`, the number of steps to eval the model.
	- __eval_delay_secs__: `int`, used to delay the evaluation.
	- __continuous_eval_throttle_secs__: Do not re-evaluate unless the last evaluation
		was started at least this many seconds ago for continuous_eval().
	- __delay_workers_by_global_step__: if `True` delays training workers based on global step
		instead of time.
	- __export_strategies__: A list of `ExportStrategy`s, or a single one, or None.
	- __train_steps_per_iteration__: (applies only to continuous_train_and_evaluate).


----

## create_run_config


```python
create_run_config(tf_random_seed=None, save_checkpoints_secs=None, save_checkpoints_steps=600, keep_checkpoint_max=5, keep_checkpoint_every_n_hours=4, gpu_memory_fraction=1.0, gpu_allow_growth=False, log_device_placement=False)
```


Creates a `RunConfig` instance.
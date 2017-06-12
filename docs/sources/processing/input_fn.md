## create_input_data_fn


```python
create_input_data_fn(mode, pipeline_config, scope=None, input_type=None, x=None, y=None)
```


Creates an input data function that can be used with estimators.
Note that you must pass "factory functions" for both the data provider and
featurizer to ensure that everything will be created in  the same graph.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __pipeline_config__: the configuration to create a Pipeline instance.
	- __scope__: `str`. scope to use for this input data block.
	- __input_type__: `str`. The type of the input, values: `NUMPY`, `PANDAS`.
		If `None`, will create a function based on the pipeline config.
	- __x__: `np.ndarray` or `np.Dataframe` or `None`.
	- __y__: `np.ndarray` or `None`.

- __Returns__:
	An input function that returns `(feature_batch, labels_batch)`
	tuples when called.

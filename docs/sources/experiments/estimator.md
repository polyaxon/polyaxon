<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/estimator.py#L44)</span>
## Estimator

```python
polyaxon.experiments.estimator.Estimator(model_fn=None, model_dir=None, config=None, params=None)
```

Estimator class is the basic TensorFlow model trainer/evaluator.

Constructs an `Estimator` instance.

- __Args__:
	- __model_fn__: Model function. Follows the signature:
		* Args:
		* `features`: single `Tensor` or `dict` of `Tensor`s
			 (depending on data passed to `fit`),
		* `labels`: `Tensor` or `dict` of `Tensor`s (for multi-head models).
			If mode is `ModeKeys.PREDICT`, `labels=None` will be passed.
			If the `model_fn`'s signature does not accept `mode`,
			the `model_fn` must still be able to handle `labels=None`.
		* `mode`: Specifies if this training, evaluation or prediction. See `ModeKeys`.
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

	- __model_dir__: Directory to save model parameters, graph and etc. This can
		also be used to load checkpoints from the directory into a estimator to
		continue training a previously saved model.
	- __config__: Configuration object.
	- __params__: `dict` of hyper parameters that will be passed into `model_fn`.
		  Keys are names of parameters, values are basic python types.
- __Raises__:
	- __ValueError__: parameters of `model_fn` don't match `params`.


----

### export_savedmodel


```python
export_savedmodel(self, export_dir_base, serving_input_receiver_fn, assets_extra=None, as_text=False, checkpoint_path=None)
```


Exports inference graph as a SavedModel into given dir.
This method builds a new graph by first calling the
serving_input_receiver_fn to obtain feature `Tensor`s, and then calling
this `Estimator`'s model_fn to generate the model graph based on those
features. It restores the given checkpoint (or, lacking that, the most
recent checkpoint) into this graph in a fresh session.  Finally it creates
a timestamped export directory below the given export_dir_base, and writes
a `SavedModel` into it containing a single `MetaGraphDef` saved from this
session.
The exported `MetaGraphDef` will provide one `SignatureDef` for each
element of the export_outputs dict returned from the model_fn, named using
the same keys.  One of these keys is always
signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY, indicating which
signature will be served when a serving request does not specify one.
For each signature, the outputs are provided by the corresponding
`ExportOutput`s, and the inputs are always the input receivers provided by
the serving_input_receiver_fn.
Extra assets may be written into the SavedModel via the extra_assets
argument.  This should be a dict, where each key gives a destination path
(including the filename) relative to the assets.extra directory.  The
corresponding value gives the full path of the source file to be copied.
For example, the simple case of copying a single file without renaming it
is specified as `{'my_asset_file.txt': '/path/to/my_asset_file.txt'}`.
- __Args__:
	- __export_dir_base__: A string containing a directory in which to create
	timestamped subdirectories containing exported SavedModels.
	- __serving_input_receiver_fn__: A function that takes no argument and
	returns a `ServingInputReceiver`.
	- __assets_extra__: A dict specifying how to populate the assets.extra directory
	within the exported SavedModel, or `None` if no extra assets are needed.
	- __as_text__: whether to write the SavedModel proto in text format.
	- __checkpoint_path__: The checkpoint path to export.  If `None` (the default),
	the most recent checkpoint found within the model directory is chosen.
- __Returns__:
	The string path to the exported directory.
- __Raises__:
	- __ValueError__: if no serving_input_receiver_fn is provided, no export_outputs
	are provided, or no checkpoint can be found.


----

### train


```python
train(self, input_fn=None, steps=None, hooks=None, max_steps=None)
```


Trains a model given training data `x` predictions and `y` labels.

- __Args__:
	- __input_fn__: Input function returning a tuple of:
	features - `Tensor` or dictionary of string feature name to `Tensor`.
	labels - `Tensor` or dictionary of `Tensor` with labels.
	- __steps__: Number of steps for which to train model. If `None`, train forever.
	'steps' works incrementally. If you call two times fit(steps=10) then
	training occurs in total 20 steps. If you don't want to have incremental
	behaviour please set `max_steps` instead. If set, `max_steps` must be
	`None`.
	- __hooks__: List of `BaseMonitor` subclass instances.
	Used for callbacks inside the training loop.
	- __max_steps__: Number of total steps for which to train model. If `None`,
	train forever. If set, `steps` must be `None`.

	Two calls to `fit(steps=100)` means 200 training iterations.
	On the other hand, two calls to `fit(max_steps=100)` means
	that the second call will not do any iteration since first call did all 100 steps.

- __Returns__:
	`self`, for chaining.


----

### evaluate


```python
evaluate(self, input_fn=None, steps=None, hooks=None, checkpoint_path=None, name=None)
```


Evaluates given model with provided evaluation data.

Stop conditions - we evaluate on the given input data until one of the
- __following__:
- If `steps` is provided, and `steps` batches of size `batch_size` are
processed.
- If `input_fn` is provided, and it raises an end-of-input
exception (`OutOfRangeError` or `StopIteration`).
- If `x` is provided, and all items in `x` have been processed.

The return value is a dict containing the metrics specified in `metrics`, as
well as an entry `global_step` which contains the value of the global step
for which this evaluation was performed.

- __Args__:
	- __input_fn__: Input function returning a tuple of:
	features - Dictionary of string feature name to `Tensor` or `Tensor`.
	labels - `Tensor` or dictionary of `Tensor` with labels.
	If `steps` is not provided, this should raise `OutOfRangeError` or
	`StopIteration` after the desired amount of data (e.g., one epoch) has
	been provided. See "Stop conditions" above for specifics.
	- __steps__: Number of steps for which to evaluate model. If `None`, evaluate
	until `x` is consumed or `input_fn` raises an end-of-input exception.
	See "Stop conditions" above for specifics.
	- __name__: Name of the evaluation if user needs to run multiple evaluations on
	different data sets, such as on training data vs test data.
	- __checkpoint_path__: Path of a specific checkpoint to evaluate. If `None`,
	the latest checkpoint in `model_dir` is used.
	- __hooks__: List of `SessionRunHook` subclass instances.
	Used for callbacks inside the evaluation call.

- __Raises__:
	- __ValueError__: If `metrics` is not `None` or `dict`.

- __Returns__:
	Returns `dict` with evaluation results.


----

### predict


```python
predict(self, input_fn=None, predict_keys=None, hooks=None, checkpoint_path=None)
```


Returns predictions for given features.

- __Args__:
	- __input_fn__: Input function returning features which is a dictionary of
	string feature name to `Tensor` or `SparseTensor`. If it returns a
	tuple, first item is extracted as features. Prediction continues until
	`input_fn` raises an end-of-input exception (`OutOfRangeError` or `StopIteration`).
	- __predict_keys__: list of `str`, name of the keys to predict. It is used if
	the `EstimatorSpec.predictions` is a `dict`. If `predict_keys` is used then rest
	of the predictions will be filtered from the dictionary. If `None`, returns all.
	- __hooks__: List of `SessionRunHook` subclass instances. Used for callbacks
	inside the prediction call.
	- __checkpoint_path__: Path of a specific checkpoint to predict. If `None`, the
	latest checkpoint in `model_dir` is used.

- __Yields__:
	Evaluated values of `predictions` tensors.

- __Raises__:
	- __ValueError__: Could not find a trained model in model_dir.
	- __ValueError__: if batch length of predictions are not same.
	- __ValueError__: If there is a conflict between `predict_keys` and `predictions`.
	For example if `predict_keys` is not `None`
	but `EstimatorSpec.predictions` is not a `dict`.


----

### get_variable_value


```python
get_variable_value(self, name)
```


Returns value of the variable given by name.

- __Args__:
	- __name__: string, name of the tensor.

- __Returns__:
	Numpy array - value of the tensor.


----

### get_variable_names


```python
get_variable_names(self)
```


Returns list of all variable names in this model.

- __Returns__:
	List of names.

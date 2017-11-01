<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/regressors.py#L12) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/models.py#L12)</span>
## Regressor

```python
polyaxon.models.regressors.Regressor(mode, graph_fn, loss=None, optimizer=None, metrics=None, summaries='all', clip_gradients=0.5, clip_embed_gradients=0.1, name='Regressor')
```

Regressor base model.

- __\__(programmatic)


	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

	- __graph_fn__: Graph function. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.

- __\__(polyaxonfile)


	- __graph__: Graph definition. see [Graph]()


- __\__(commun)


	- __loss__: An instance of `LossConfig`. Default value `MeanSquaredErrorConfig`.

	- __optimizer__: An instance of `OptimizerConfig`.

		Default value `AdamConfig(learning_rate=0.001)`.
	- __metrics__: a list of `MetricConfig` instances.

	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.

		Possible values:
		 [`all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`]
	- __clip_gradients__: `float`. Gradients  clipping by global norm.

	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.

	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.


- __Returns__:

	`EstimatorSpec`

Programmatic usage:

```python
def graph_fn(mode, features):
	x = features['x']
	x = plx.layers.LSTM(units=10)(x)
	return plx.layers.Dense(units=1)(x)

model = plx.models.Regressor(
	mode=mode,
	graph_fn=graph_fn,
	loss=MeanSquaredErrorConfig(),
	optimizer=AdagradConfig(learning_rate=0.1),
	metrics=[
		RootMeanSquaredErrorConfig(),
		MeanAbsoluteErrorConfig()])
```

Polyaxonfile usage:

```yaml
model:
  regressor:
	loss: MeanSquaredError
	optimizer:
	  Adagrad:
		learning_rate: 0.1
	metrics:
	  - RootMeanSquaredError
	  - MeanAbsoluteError
	graph:
	  input_layers: x
	  layers:
		- LSTM:
			units: 19
		- Dense:
			units: 1
```

or use model_type to reduce the nesting level

```yaml
model:
  model_type: regressor:
  loss: MeanSquaredError
  optimizer:
	Adagrad:
	  learning_rate: 0.1
  metrics:
	- RootMeanSquaredError
	- MeanAbsoluteError
  graph:
	input_layers: x
	layers:
	  - LSTM:
		  units: 19
	  - Dense:
		  units: 1
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/classifiers.py#L14) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/models.py#L14)</span>
## Classifier

```python
polyaxon.models.classifiers.Classifier(mode, graph_fn, loss=None, optimizer=None, summaries='all', metrics=None, clip_gradients=0.5, clip_embed_gradients=0.1, one_hot_encode=None, n_classes=None, name='Classifier')
```

Regressor base model.

- __\__(programmatic)


	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

	- __graph_fn__: Graph function. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.

- __\__(polyaxonfile)


	- __graph__: Graph definition. see [Graph]()


- __\__(commun)


	- __loss__: An instance of `LossConfig`. Default value `SigmoidCrossEntropyConfig`.

	- __optimizer__: An instance of `OptimizerConfig`.

		Default value `AdamConfig(learning_rate=0.001)`.
	- __metrics__: a list of `MetricConfig` instances.

	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.

		Possible values:
		 [`all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`]
	- __clip_gradients__: `float`. Gradients  clipping by global norm.

	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.

	- __one_hot_encode__: `bool`. to one hot encode the outputs.

	- __n_classes__: `int`. The number of classes used in the one hot encoding.

	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.


- __Returns__:

	`EstimatorSpec`

Programmatic usage:

```python
def graph_fn(mode, features):
	x = plx.layers.Conv2D(filters=32, kernel_size=5)(features['image'])
	x = plx.layers.MaxPooling2D(pool_size=2)(x)
	x = plx.layers.Conv2D(filters=64, kernel_size=5)(x)
	x = plx.layers.MaxPooling2D(pool_size=2)(x)
	x = plx.layers.Flatten()(x)
	x = plx.layers.Dense(units=10)(x)
	return x

model = plx.models.Classifier(
	mode=mode,
	graph_fn=graph_fn,
	loss=SigmoidCrossEntropyConfig(),
	optimizer=AdamConfig(
		learning_rate=0.007, decay_type='exponential_decay', decay_rate=0.1),
	metrics=[AccuracyConfig(), PrecisionConfig()],
	summaries='all',
	one_hot_encode=True,
	n_classes=10)
```

Polyaxonfile usage:

```yaml
model:
  classifier:
	loss: SigmoidCrossEntropy
	optimizer:
	  Adam:
		learning_rate: 0.007
		decay_type: exponential_decay
		decay_rate: 0.2
	metrics:
	  - Accuracy
	  - Precision
	one_hot_encode: true
	n_classes: 10
	graph:
	  input_layers: image
	  layers:
		- Conv2D:
			filters: 32
			kernel_size: 5
			strides: 1
		- MaxPooling2D:
			pool_size: 2
		- Conv2D:
			filters: 64
			kernel_size: 5
		- MaxPooling2D:
			pool_size: 2
		- Flatten:
		- Dense:
			units: 1024
			activation: tanh
		- Dense:
		   units: 10
```

or use model_type to reduce the nesting level

```yaml
model:
  model_type: classifier
  loss: SigmoidCrossEntropy
  optimizer:
	Adam:
	  learning_rate: 0.007
	  decay_type: exponential_decay
	  decay_rate: 0.2
  metrics:
	- Accuracy
	- Precision
  one_hot_encode: true
  n_classes: 10
  graph:
	input_layers: image
	layers:
	  - Conv2D:
		  filters: 32
		  kernel_size: 5
		  strides: 1
	  - MaxPooling2D:
		  pool_size: 2
	  - Conv2D:
		  filters: 64
		  kernel_size: 5
	  - MaxPooling2D:
		  pool_size: 2
	  - Flatten:
	  - Dense:
		  units: 1024
		  activation: tanh
	  - Dense:
		 units: 10
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/generators.py#L20) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/models.py#L20)</span>
## Generator

```python
polyaxon.models.generators.Generator(mode, encoder_fn, decoder_fn, bridge_fn, loss=None, optimizer=None, summaries='all', metrics=None, clip_gradients=0.5, clip_embed_gradients=0.1, name='Generator')
```

Generator base model.

- __\__(programmatic)


	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.

	- __encoder_fn__: Encoder Graph function. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.
	- __decoder_fn__: Decoder Graph function. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.
	- __bridge_fn__: The bridge to use. Follows the signature:

		* Args:
			* `mode`: Specifies if this training, evaluation or prediction. See `Modes`.
			* `inputs`: the feature inputs.
			* `encoder_fn`: the encoder function.
			* `decoder_fn` the decoder function.
- __\__(polyaxonfile)


	- __encoder__: Graph definition. see [Graph]()

	- __decoder__: Graph definition. see [Graph]()

	- __bridge__: Graph definition. see [Graph]()


- __\__(commun)


	- __loss__: An instance of `LossConfig`. Default value `SigmoidCrossEntropyConfig`.

	- __optimizer__: An instance of `OptimizerConfig`.

		Default value `AdadeltaConfig(learning_rate=0.4)`.
	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.

		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __metrics__: a list of `MetricConfig` instances.

	- __summaries__: `str` or `list`. The verbosity of the tensorboard visualization.

		Possible values: `all`, `activations`, `loss`, `learning_rate`, `variables`, `gradients`
	- __clip_gradients__: `float`. Gradients  clipping by global norm.

	- __clip_embed_gradients__: `float`. Embedding gradients clipping to a specified value.

	- __name__: `str`, the name of this model, everything will be encapsulated inside this scope.


- __Returns__:

	`EstimatorSpec`

Programmatic usage:

```python
def encoder_fn(mode, features):
x = plx.layers.Dense(units=128)(features)
x = plx.layers.Dense(units=256)(x)
return x


def decoder_fn(mode, features):
	x = plx.layers.Dense(units=256)(features)
	return plx.layers.Dense(units=784)(x)


def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
	return plx.bridges.NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)

model = plx.models.Generator(
	mode=mode,
	encoder_fn=encoder_fn,
	decoder_fn=decoder_fn,
	bridge_fn=bridge_fn,
	loss=MeanSquaredErrorConfig(),
	optimizer=AdadeltaConfig(learning_rate=0.9),
	summaries=['loss'])
```

Polyaxonfile usage:

```yaml
model:
  generator:
	loss:
	  MeanSquaredError:
	optimizer:
	  Adam:
		learning_rate: 0.9
	metrics:
	  - Accuracy
	bridge: NoOpBridge
	encoder:
	  input_layers: image
	  layers:
		- Dense:
			units: 128
		- Dense:
			units: 256
			name: encoded
	decoder:
	  input_layers: encoded
	  layers:
		- Dense:
			units: 256
		- Dense:
			units: 784
```

or use model_type to reduce the nesting level

```yaml
model:
  model_type: generator:
  loss:
	MeanSquaredError:
  optimizer:
	Adam:
	  learning_rate: 0.9
  metrics:
	- Accuracy
  bridge: NoOpBridge
  encoder:
	input_layers: image
	layers:
	  - Dense:
		  units: 128
	  - Dense:
		  units: 256
		  name: encoded
  decoder:
	input_layers: encoded
	layers:
	  - Dense:
		  units: 256
	  - Dense:
		  units: 784
```

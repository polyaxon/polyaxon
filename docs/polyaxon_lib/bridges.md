<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/bridges.py#L113)</span>
## NoOpBridgeConfig

```python
polyaxon_schemas.bridges.NoOpBridgeConfig(state_size=None, name=None)
```

A bridge that passes the encoder output to the decoder.

This bridge could be used by VAE.

- __Args__(programmatic)


	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.


- __Args__:

	- __state_size__: `int`. The latent dimension to use.

	- __name__: `str`. The name of this subgraph, used for creating the scope.


- __Returns__:

	`BridgeSpec`

Programmatic usage:

```python
def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
	return plx.bridges.NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)
```

Polyaxonfile usage:

```yaml
model:
  generator:
	...
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


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/bridges.py#L40)</span>
## LatentBridgeConfig

```python
polyaxon_schemas.bridges.LatentBridgeConfig(latent_dim=1, mean=0.0, stddev=1.0)
```

A bridge that create a latent space based on the encoder output.

This bridge could be used by VAE.

- __Args__(programmatic)


	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.


- __Args__:

	- __latent_dim__: `int`. The latent dimension to use.

	- __name__: `str`. The name of this subgraph, used for creating the scope.


- __Attributes__:

	- __z_mean__: `Tensor`. The latent distribution mean.

	- __z_log_sigma__: `Tensor`. The latent distribution log variance.


- __Returns__:

	`BridgeSpec`

Programmatic usage:

```python
def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
	return plx.bridges.LatentBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)
```

Polyaxonfile usage:

```yaml
model:
  generator:
	...
	bridge: LatentBridge
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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/bridges/noop_bridge.py#L10) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/bridges.py#L10)</span>
## NoOpBridge

```python
polyaxon.bridges.noop_bridge.NoOpBridge(mode, state_size=None, name='NoOpBridge')
```

A bridge that passes the encoder output to the decoder.

This bridge could be used by VAE.

- __\__(programmatic)


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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/bridges/latent_bridge.py#L15) [[schema source]](https://github.com/polyaxon/polyaxon-schemas/blob/master/polyaxon_schemas/bridges.py#L15)</span>
## LatentBridge

```python
polyaxon.bridges.latent_bridge.LatentBridge(mode, latent_dim=1, state_size=None, mean=0.0, stddev=1.0, name='LatentBridge')
```

A bridge that create a latent space based on the encoder output.

This bridge could be used by VAE.

- __\__(programmatic)


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

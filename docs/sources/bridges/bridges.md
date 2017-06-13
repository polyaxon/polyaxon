<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/bridges/noop_bridge.py#L7)</span>
## NoOpBridge

```python
polyaxon.bridges.noop_bridge.NoOpBridge(mode, state_size=None, name='NoOpBridge')
```

A bridge that passes the encoder to the decoder outputs.

- __Args__:
	- __mode__: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __name__: `str`. The name of this bridge, used for creating the scope.
	- __state_size__: `int`. The bridge state size. Default None, it will be inferred
	directly from the incoming tensor.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/bridges/latent_bridge.py#L11)</span>
## LatentBridge

```python
polyaxon.bridges.latent_bridge.LatentBridge(mode, latent_dim=1, state_size=None, mean=0.0, stddev=1.0, name='LatentBridge')
```

A bridge that create a latent space based on the encoder output.

A bridge defines how latent state between the encoder and decoder.
This bridge should be used by VAE.

- __Args__:
	- __latent_dim__: `int`. The latent dimension to use.
	- __mode__: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
	- __name__: `str`. The name of this subgraph, used for creating the scope.

- __Attributes__:
	- __z_mean__: `Tensor`. The latent distribution mean.
	- __z_log_sigma__: `Tensor`. The latent distribution log variance.

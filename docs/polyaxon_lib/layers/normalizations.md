<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/normalization.py#L43)</span>
## BatchNormalizationConfig

```python
polyaxon_schemas.layers.normalization.BatchNormalizationConfig(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True, beta_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x1077d1240>, gamma_initializer=<polyaxon_schemas.initializations.OnesInitializerConfig object at 0x1077d1208>, moving_mean_initializer=<polyaxon_schemas.initializations.ZerosInitializerConfig object at 0x1077d1278>, moving_variance_initializer=<polyaxon_schemas.initializations.OnesInitializerConfig object at 0x1077d12b0>, beta_regularizer=None, gamma_regularizer=None, beta_constraint=None, gamma_constraint=None)
```

Batch normalization layer (Ioffe and Szegedy, 2014).

Normalize the activations of the previous layer at each batch,
i.e. applies a transformation that maintains the mean activation
close to 0 and the activation standard deviation close to 1.

- __Args__:

	- __axis__: Integer, the axis that should be normalized

		(typically the features axis).
		For instance, after a `Conv2D` layer with
		`data_format="channels_first"`,
		set `axis=1` in `BatchNormalization`.
	- __momentum__: Momentum for the moving average.

	- __epsilon__: Small float added to variance to avoid dividing by zero.

	- __center__: If True, add offset of `beta` to normalized tensor.

		If False, `beta` is ignored.
	- __scale__: If True, multiply by `gamma`.

		If False, `gamma` is not used.
		When the next layer is linear (also e.g. `nn.relu`),
		this can be disabled since the scaling
		will be done by the next layer.
	- __beta_initializer__: Initializer for the beta weight.

	- __gamma_initializer__: Initializer for the gamma weight.

	- __moving_mean_initializer__: Initializer for the moving mean.

	- __moving_variance_initializer__: Initializer for the moving variance.

	- __beta_regularizer__: Optional regularizer for the beta weight.

	- __gamma_regularizer__: Optional regularizer for the gamma weight.

	- __beta_constraint__: Optional constraint for the beta weight.

	- __gamma_constraint__: Optional constraint for the gamma weight.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as input.

- __References__:

	- [Batch Normalization: Accelerating Deep Network Training by Reducing
	  Internal Covariate Shift](https://arxiv.org/abs/1502.03167)

Polyaxonfile usage:

```yaml
BatchNormalization:
  momentum: 0.7
```

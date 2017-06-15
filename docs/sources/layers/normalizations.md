<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/normalizations.py#L16)</span>
## BatchNormalization

```python
polyaxon.layers.normalizations.BatchNormalization(mode, beta=0.0, gamma=1.0, epsilon=1e-05, decay=0.9, stddev=0.002, trainable=True, restore=True, name='BatchNormalization')
```

Adds a Batch Normalization.

Normalize activations of the previous layer at each batch.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __beta__: `float`. Default: 0.0.
	- __gamma__: `float`. Default: 1.0.
	- __epsilon__: `float`. Defalut: 1e-5.
	- __decay__: `float`. Default: 0.9.
	- __stddev__: `float`. Standard deviation for weights initialization.
	- __trainable__: `bool`. If True, weights will be trainable.
	- __restore__: `bool`. If True, this layer weights will be restored when
		loading a model.
	- __name__: `str`. A name for this layer (optional).

- __References__:
	Batch Normalization: Accelerating Deep Network Training by Reducing
	Internal Covariate Shif. Sergey Ioffe, Christian Szegedy. 2015.

- __Links__:
	- __[http__://arxiv.org/pdf/1502.03167v3.pdf](http://arxiv.org/pdf/1502.03167v3.pdf)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/normalizations.py#L101)</span>
## LocalResponseNormalization

```python
polyaxon.layers.normalizations.LocalResponseNormalization(mode, depth_radius=5, bias=1.0, alpha=0.0001, beta=0.75, name='LocalResponseNormalization')
```

Local Response Normalization.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __depth_radius__: `int`. 0-D.  Half-width of the 1-D normalization window.
		Defaults to 5.
	- __bias__: `float`. An offset (usually positive to avoid dividing by 0).
		Defaults to 1.0.
	- __alpha__: `float`. A scale factor, usually positive. Defaults to 0.0001.
	- __beta__: `float`. An exponent. Defaults to `0.5`.
	- __name__: `str`. A name for this layer (optional).


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/normalizations.py#L135)</span>
## L2Normalization

```python
polyaxon.layers.normalizations.L2Normalization(mode, dim, epsilon=1e-12, name='l2Normalize')
```

Adds an L2 Normalization.

Normalizes along dimension `dim` using an L2 norm.

For a 1-D tensor with `dim = 0`, computes
```python
>>> output = x / sqrt(max(sum(x**2), epsilon))
```

For `x` with more dimensions, independently normalizes each 1-D slice along
dimension `dim`.

- __Args__:
	- __mode__: `str`, Specifies if this training, evaluation or prediction. See `Modes`.
	- __dim__: `int`. Dimension along which to normalize.
	- __epsilon__: `float`. A lower bound value for the norm. Will use
		`sqrt(epsilon)` as the divisor if `norm < sqrt(epsilon)`.
	- __name__: `str`. A name for this layer (optional).

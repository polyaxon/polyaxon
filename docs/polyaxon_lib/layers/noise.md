<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/noise.py#L24)</span>
## GaussianNoiseConfig

```python
polyaxon_schemas.layers.noise.GaussianNoiseConfig(stddev)
```

Apply additive zero-centered Gaussian noise.

This is useful to mitigate overfitting
(you could see it as a form of random data augmentation).
Gaussian Noise (GS) is a natural choice as corruption process
for real valued inputs.

As it is a regularization layer, it is only active at training time.

- __Args__:

	- __stddev__: float, standard deviation of the noise distribution.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as input.

Polyaxonfile usage:

```yaml
GaussianNoise:
  stddev: 0.5
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/noise.py#L75)</span>
## GaussianDropoutConfig

```python
polyaxon_schemas.layers.noise.GaussianDropoutConfig(rate)
```

Apply multiplicative 1-centered Gaussian noise.

As it is a regularization layer, it is only active at training time.

- __Args__:

	- __rate__: float, drop probability (as with `Dropout`).

		The multiplicative noise will have
		standard deviation `sqrt(rate / (1 - rate))`.

Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as input.

- __References__:

	- [Dropout: A Simple Way to Prevent Neural Networks from Overfitting
	  Srivastava, Hinton, et al.
	  2014](http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf)

Polyaxonfile usage:

```yaml
GaussianDropout:
  rate: 0.7
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/noise.py#L130)</span>
## AlphaDropoutConfig

```python
polyaxon_schemas.layers.noise.AlphaDropoutConfig(rate, noise_shape=None, seed=None)
```

Applies Alpha Dropout to the input.

Alpha Dropout is a `Dropout` that keeps mean and variance of inputs
to their original values, in order to ensure the self-normalizing property
even after this dropout.
Alpha Dropout fits well to Scaled Exponential Linear Units
by randomly setting activations to the negative saturation value.

- __Args__:

	- __rate__: float, drop probability (as with `Dropout`).

		The multiplicative noise will have
		standard deviation `sqrt(rate / (1 - rate))`.
	- __seed__: A Python integer to use as random seed.


Input shape:
	Arbitrary. Use the keyword argument `input_shape`
	(tuple of integers, does not include the samples axis)
	when using this layer as the first layer in a model.

Output shape:
	Same shape as input.

- __References__:

	- [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)

Polyaxonfile usage:

```yaml
AlphaDropout:
  rate: 0.7
```

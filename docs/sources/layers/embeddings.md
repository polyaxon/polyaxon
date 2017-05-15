<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/embedding.py#L13)</span>
### Embedding

```python
polyaxon.layers.embedding.Embedding(mode, input_dim, output_dim, validate_indices=False, weights_init='truncated_normal', trainable=True, restore=True, name='Embedding')
```

Embedding layer for a sequence of integer ids or floats.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __input_dim__: list of `int`. Vocabulary size (number of ids).
- __output_dim__: list of `int`. Embedding size.
- __validate_indices__: `bool`. Whether or not to validate gather indices.
- __weights_init__: `str` (name) or `Tensor`. Weights initialization.
	- __Default__: 'truncated_normal'.
- __trainable__: `bool`. If True, weights will be trainable.
- __restore__: `bool`. If True, this layer weights will be restored when
	loading a model.
- __name__: A name for this layer (optional). Default: 'Embedding'.

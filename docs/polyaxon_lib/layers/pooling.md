<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L79)</span>
## AveragePooling1DConfig

```python
polyaxon_schemas.layers.pooling.AveragePooling1DConfig(pool_size=2, strides=None, padding='valid')
```

Average pooling for temporal data.

- __Args__:

	- __pool_size__: Integer, size of the max pooling windows.

	- __strides__: Integer, or None. Factor by which to downscale.

		E.g. 2 will halve the input.
		If None, it will default to `pool_size`.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).


Input shape:
	3D tensor with shape: `(batch_size, steps, features)`.

Output shape:
	3D tensor with shape: `(batch_size, downsampled_steps, features)`.

Polyaxonfile usage:

```yaml
AveragePooling1D:
  pool_size: 2
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L28)</span>
## MaxPooling1DConfig

```python
polyaxon_schemas.layers.pooling.MaxPooling1DConfig(pool_size=2, strides=None, padding='valid')
```

Max pooling operation for temporal data.

- __Args__:

	- __pool_size__: Integer, size of the max pooling windows.

	- __strides__: Integer, or None. Factor by which to downscale.

		E.g. 2 will halve the input.
		If None, it will default to `pool_size`.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).


Input shape:
	3D tensor with shape: `(batch_size, steps, features)`.

Output shape:
	3D tensor with shape: `(batch_size, downsampled_steps, features)`.

Polyaxonfile usage:

```yaml
MaxPooling1D:
  pool_size: 2
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L208)</span>
## AveragePooling2DConfig

```python
polyaxon_schemas.layers.pooling.AveragePooling2DConfig(pool_size=(2, 2), strides=None, padding='valid', data_format=None)
```

Average pooling operation for spatial data.

- __Args__:

	- __pool_size__: integer or tuple of 2 integers,

		factors by which to downscale (vertical, horizontal).
		(2, 2) will halve the input in both spatial dimension.
		If only one integer is specified, the same window length
		will be used for both dimensions.
	- __strides__: Integer, tuple of 2 integers, or None.

		Strides values.
		If None, it will default to `pool_size`.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, height, width, channels)` while `channels_first`
		corresponds to inputs with shape
		`(batch, channels, height, width)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, rows, cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, rows, cols)`

Output shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, pooled_rows, pooled_cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, pooled_rows, pooled_cols)`

Polyaxonfile usage:

```yaml
AveragePooling2D:
  pool_size: [2, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L132)</span>
## MaxPooling2DConfig

```python
polyaxon_schemas.layers.pooling.MaxPooling2DConfig(pool_size=(2, 2), strides=None, padding='valid', data_format=None)
```

Max pooling operation for spatial data.

- __Args__:

	- __pool_size__: integer or tuple of 2 integers,

		factors by which to downscale (vertical, horizontal).
		(2, 2) will halve the input in both spatial dimension.
		If only one integer is specified, the same window length
		will be used for both dimensions.
	- __strides__: Integer, tuple of 2 integers, or None.

		Strides values.
		If None, it will default to `pool_size`.
	- __padding__: One of `"valid"` or `"same"` (case-insensitive).

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, height, width, channels)` while `channels_first`
		corresponds to inputs with shape
		`(batch, channels, height, width)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, rows, cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, rows, cols)`

Output shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, pooled_rows, pooled_cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, pooled_rows, pooled_cols)`

Polyaxonfile usage:

```yaml
MaxPooling2D:
  pool_size: [2, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L357)</span>
## AveragePooling3DConfig

```python
polyaxon_schemas.layers.pooling.AveragePooling3DConfig(pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None)
```

Average pooling operation for 3D data (spatial or spatio-temporal).

- __Args__:

	- __pool_size__: tuple of 3 integers,

		factors by which to downscale (dim1, dim2, dim3).
		(2, 2, 2) will halve the size of the 3D input in each dimension.
	- __strides__: tuple of 3 integers, or None. Strides values.

	- __padding__: One of `"valid"` or `"same"` (case-insensitive).

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
		while `channels_first` corresponds to inputs with shape
		`(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

Output shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, pooled_dim1, pooled_dim2, pooled_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, pooled_dim1, pooled_dim2, pooled_dim3)`

Polyaxonfile usage:

```yaml
AveragePooling3D:
  pool_size: [2, 2, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L284)</span>
## MaxPooling3DConfig

```python
polyaxon_schemas.layers.pooling.MaxPooling3DConfig(pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None)
```

Max pooling operation for 3D data (spatial or spatio-temporal).

- __Args__:

	- __pool_size__: tuple of 3 integers,

		factors by which to downscale (dim1, dim2, dim3).
		(2, 2, 2) will halve the size of the 3D input in each dimension.
	- __strides__: tuple of 3 integers, or None. Strides values.

	- __padding__: One of `"valid"` or `"same"` (case-insensitive).

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
		while `channels_first` corresponds to inputs with shape
		`(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

Output shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, pooled_dim1, pooled_dim2, pooled_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, pooled_dim1, pooled_dim2, pooled_dim3)`

Polyaxonfile usage:

```yaml
MaxPooling3D:
  pool_size: [2, 2, 2]
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L423)</span>
## GlobalAveragePooling1DConfig

```python
polyaxon_schemas.layers.pooling.GlobalAveragePooling1DConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Global average pooling operation for temporal data.

Input shape:
	3D tensor with shape: `(batch_size, steps, features)`.

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalAveragePooling1D:
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L456)</span>
## GlobalMaxPooling1DConfig

```python
polyaxon_schemas.layers.pooling.GlobalMaxPooling1DConfig(name=None, trainable=True, dtype='float32', inbound_nodes=None)
```

Global max pooling operation for temporal data.

Input shape:
	3D tensor with shape: `(batch_size, steps, features)`.

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalMaxPooling1D:
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L492)</span>
## GlobalAveragePooling2DConfig

```python
polyaxon_schemas.layers.pooling.GlobalAveragePooling2DConfig(data_format=None)
```

Global average pooling operation for spatial data.

- __Args__:

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, height, width, channels)` while `channels_first`
		corresponds to inputs with shape
		`(batch, channels, height, width)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, rows, cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, rows, cols)`

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalAveragePooling2D:
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L547)</span>
## GlobalMaxPooling2DConfig

```python
polyaxon_schemas.layers.pooling.GlobalMaxPooling2DConfig(data_format=None)
```

Global max pooling operation for spatial data.

- __Args__:

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, height, width, channels)` while `channels_first`
		corresponds to inputs with shape
		`(batch, channels, height, width)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		4D tensor with shape:
		`(batch_size, rows, cols, channels)`
	- If `data_format='channels_first'`:
		4D tensor with shape:
		`(batch_size, channels, rows, cols)`

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalMaxPooling2D:
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L602)</span>
## GlobalAveragePooling3DConfig

```python
polyaxon_schemas.layers.pooling.GlobalAveragePooling3DConfig(data_format=None)
```

Global Average pooling operation for 3D data.

- __Args__:

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
		while `channels_first` corresponds to inputs with shape
		`(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalAveragePooling3D:
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/layers/pooling.py#L657)</span>
## GlobalMaxPooling3DConfig

```python
polyaxon_schemas.layers.pooling.GlobalMaxPooling3DConfig(data_format=None)
```

Global Max pooling operation for 3D data.

- __Args__:

	- __data_format__: A string,

		one of `channels_last` (default) or `channels_first`.
		The ordering of the dimensions in the inputs.
		`channels_last` corresponds to inputs with shape
		`(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
		while `channels_first` corresponds to inputs with shape
		`(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
		If you never set it, then it will be "channels_last".

Input shape:
	- If `data_format='channels_last'`:
		5D tensor with shape:
		`(batch_size, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	- If `data_format='channels_first'`:
		5D tensor with shape:
		`(batch_size, channels, spatial_dim1, spatial_dim2, spatial_dim3)`

Output shape:
	2D tensor with shape:
	`(batch_size, channels)`

Polyaxonfile usage:

```yaml
GlobalMaxPooling3D:
```

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L26)</span>
## AveragePooling1D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.AveragePooling1D(pool_size=2, strides=None, padding='valid')
```

Average pooling for temporal data.

  Arguments:
  - __pool_size__: Integer, size of the max pooling windows.
  - __strides__: Integer, or None. Factor by which to downscale.
	  E.g. 2 will halve the input.
	  If None, it will default to `pool_size`.
  - __padding__: One of `"valid"` or `"same"` (case-insensitive).

  Input shape:
  3D tensor with shape: `(batch_size, steps, features)`.

  Output shape:
  3D tensor with shape: `(batch_size, downsampled_steps, features)`.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L31)</span>
## MaxPooling1D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.MaxPooling1D(pool_size=2, strides=None, padding='valid')
```

Max pooling operation for temporal data.

  Arguments:
  - __pool_size__: Integer, size of the max pooling windows.
  - __strides__: Integer, or None. Factor by which to downscale.
	  E.g. 2 will halve the input.
	  If None, it will default to `pool_size`.
  - __padding__: One of `"valid"` or `"same"` (case-insensitive).

  Input shape:
  3D tensor with shape: `(batch_size, steps, features)`.

  Output shape:
  3D tensor with shape: `(batch_size, downsampled_steps, features)`.
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L36)</span>
## AveragePooling2D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.AveragePooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None)
```

Average pooling operation for spatial data.

  Arguments:
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
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L41)</span>
## MaxPooling2D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format=None)
```

Max pooling operation for spatial data.

  Arguments:
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
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L46)</span>
## AveragePooling3D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.AveragePooling3D(pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None)
```

Average pooling operation for 3D data (spatial or spatio-temporal).

  Arguments:
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
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L51)</span>
## MaxPooling3D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.MaxPooling3D(pool_size=(2, 2, 2), strides=None, padding='valid', data_format=None)
```

Max pooling operation for 3D data (spatial or spatio-temporal).

  Arguments:
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
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L56)</span>
## GlobalAveragePooling1D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalAveragePooling1D()
```

Global average pooling operation for temporal data.

  Input shape:
  3D tensor with shape: `(batch_size, steps, features)`.

  Output shape:
  2D tensor with shape:
  `(batch_size, channels)`
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L61)</span>
## GlobalMaxPooling1D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalMaxPooling1D()
```

Global max pooling operation for temporal data.

  Input shape:
  3D tensor with shape: `(batch_size, steps, features)`.

  Output shape:
  2D tensor with shape:
  `(batch_size, channels)`
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L66)</span>
## GlobalAveragePooling2D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalAveragePooling2D(data_format=None)
```

Global average pooling operation for spatial data.

  Arguments:
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, height, width, channels)` while `channels_first`
	  corresponds to inputs with shape
	  `(batch, channels, height, width)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L71)</span>
## GlobalMaxPooling2D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalMaxPooling2D(data_format=None)
```

Global max pooling operation for spatial data.

  Arguments:
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, height, width, channels)` while `channels_first`
	  corresponds to inputs with shape
	  `(batch, channels, height, width)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L76)</span>
## GlobalAveragePooling3D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalAveragePooling3D(data_format=None)
```

Global Average pooling operation for 3D data.

  Arguments:
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/layers/pooling.py#L81)</span>
## GlobalMaxPooling3D

```python
tensorflow.contrib.keras.python.keras.layers.pooling.GlobalMaxPooling3D(data_format=None)
```

Global Max pooling operation for 3D data.

  Arguments:
  - __data_format__: A string,
	  one of `channels_last` (default) or `channels_first`.
	  The ordering of the dimensions in the inputs.
	  `channels_last` corresponds to inputs with shape
	  `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
	  while `channels_first` corresponds to inputs with shape
	  `(batch, channels, spatial_dim1, spatial_dim2, spatial_dim3)`.
	  It defaults to the `image_data_format` value found in your
	  Keras config file at `~/.keras/keras.json`.
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
  
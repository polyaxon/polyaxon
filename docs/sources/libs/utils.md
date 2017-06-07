## track


```python
track(tensor, collection, scope=None)
```


Track tensor by adding it to the collection.

----

## get_tracked


```python
get_tracked(collection, scope=None)
```


Returns a list of values in the collection with the given `collection`.

----

## get_shape


```python
get_shape(x)
```


Get the incoming data shape.

- __Args__:
	- __x__: incoming data.
- __Returns__:
	the incoming data shape.


----

## validate_dtype


```python
validate_dtype(x)
```


----

## get_variable_scope


```python
get_variable_scope(name=None, scope=None, values=None, reuse=None)
```


----

## get_name_scope


```python
get_name_scope(name=None, scope=None, values=None)
```


----

## clip


```python
clip(x, min_value, max_value)
```


Element-wise value clipping.

----

## int_or_tuple


```python
int_or_tuple(value)
```


Converts `value` (int or tuple) to height, width.

This functions normalizes the input value by always returning a tuple.

- __Args__:
	- __value__: A list of 2 ints, 4 ints, a single int or a tf.TensorShape.

- __Returns__:
	A list with 4 values.

- __Raises__:
	- __ValueError__: If `value` it not well formed.
	- __TypeError__: if the `value` type is not supported


----

## int_or_tuple_3d


```python
int_or_tuple_3d(value)
```


Converts `value` (int or tuple) to height, width for 3d ops.

This functions normalizes the input value by always returning a tuple.

- __Args__:
	- __value__: A list of 3 ints, 5 ints, a single int or a tf.TensorShape.

- __Returns__:
	A list with 5 values.

- __Raises__:
	- __ValueError__: If `value` it not well formed.
	- __TypeError__: if the `value` type is not supported


----

## validate_padding


```python
validate_padding(value)
```


Validates and format padding value

- __Args__:
	- __value__: `str` padding value to validate.

- __Returns__:
	formatted value.

- __Raises__:
	- __ValueError__: if is not valid.


----

## validate_filter_size


```python
validate_filter_size(filter_size, in_depth, num_filter)
```


Validates filter size for CNN operations

----

## validate_filter_size_3d


```python
validate_filter_size_3d(filter_size, in_depth, num_filter)
```


Validates filter size for 3d CNN operations

----

## check_restore_tensor


```python
check_restore_tensor(tensor_to_check, exclvars)
```


----

## transpose_batch_time


```python
transpose_batch_time(x)
```


Transpose the batch and time dimensions of a Tensor.

Retains as much of the static shape information as possible.

- __Args__:
	- __x__: A tensor of rank 2 or higher.

- __Returns__:
	x transposed along the first two dimensions.

- __Raises__:
	- __ValueError__: if `x` is rank 1 or lower.


----

## generate_model_dir


```python
generate_model_dir()
```


----

## get_arguments


```python
get_arguments(func)
```


Returns list of arguments this function has.

----

## extract_batch_length


```python
extract_batch_length(values)
```


Extracts batch length of predictions.

----

## new_attr_context


```python
new_attr_context()
```


Creates a new context in which an object's attribute can be changed.

This creates a context in which an object's attribute can be changed.
Once the context is exited, the attribute reverts to its original value.

- __Args__:
	- __obj__: An object whose attribute to restore at the end of the context.
	- __attr__: An attribute to remember and restore at the end of the context.

- __Yields__:
	Context.

- __Example__:
```python
>>> my_obj.x = 1
>>> with _new_attr_context(my_obj, "x"):
>>> my_obj.x = 2
>>> print(my_obj.x)
>>> print(my_obj.x)
```

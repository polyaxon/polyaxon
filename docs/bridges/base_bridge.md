<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon-docs/blob/master/polyaxon/bridges/base.py#L23)</span>
## BaseBridge

```python
polyaxon.bridges.base.BaseBridge(mode, state_size, name='Bridge')
```

An abstract base class for defining a bridge.

A bridge defines how state is passed between encoder and decoder.

- __Args__:
	- __mode__: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
	- __name__: `str`. The name of this bridge, used for creating the scope.
	- __state_size__: `int`. The bridge state size.


----

### encode


```python
encode(self, features, labels, encoder_fn)
```


Encodes the incoming tensor.

- __Args__:
	- __features__: `Tensor`.
	- __labels__: `dict` or `Tensor`
	- __encoder_fn__: `function`.
	- __*args__:
	- __**kwargs__:


----

### decode


```python
decode(self, features, labels, decoder_fn)
```


Decodes the incoming tensor if it's validates against the state size of the decoder.
Otherwise, generates a random value.

- __Args__:
	- __features__: `Tensor`
	- __labels__: `dict` or `Tensor`
	- __decoder_fn__: `function`.
	- __*args__:
	- __**kwargs__:


----

### _get_decoder_shape


```python
_get_decoder_shape(self, incoming)
```


Returns the decoder expected shape based on the incoming tensor.

----

### _build


```python
_build(self, features, labels, loss, encoder_fn, decoder_fn)
```


Subclasses should implement their logic here and must return a `BridgeSpec`.
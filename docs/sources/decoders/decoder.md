<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/decoders/base.py#L16)</span>
## Decoder

```python
polyaxon.decoders.base.Decoder(mode, modules, name='Decoder', features=None)
```

An abstract base class for defining a decoder.

- __Args__:
	- __mode__: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
	- __name__: `str`. The name of this bridge, used for creating the scope.


----

### _build


```python
_build(self, incoming)
```


Creates the encoder logic and returns an `DecoderSpec`.

----

### decode


```python
decode(self, incoming)
```


Subclasses should implement their logic here.
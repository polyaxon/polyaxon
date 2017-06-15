<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/encoders/base.py#L16)</span>
## Encoder

```python
polyaxon.encoders.base.Encoder(mode, modules, name='Encoder', features=None)
```

An abstract base class for defining an encoder.

- __Args__:
	- __mode__: `str`. Specifies if this training, evaluation or prediction. See `Modes`.
	- __name__: `str`. The name of this encoder, used for creating the scope.


----

### _build


```python
_build(self, incoming)
```


Creates the encoder logic and returns an `EncoderSpec`.

----

### encode


```python
encode(self, incoming)
```


Subclasses should implement their logic here.
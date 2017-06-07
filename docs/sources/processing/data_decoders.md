<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_decoders.py#L13)</span>
## DataDecoder

```python
polyaxon.processing.data_decoders.DataDecoder()
```

An abstract class which is used to decode data for a provider.

(A mirror to tf.slim.data DataDecoder)


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_decoders.py#L46)</span>
## TFExampleDecoder

```python
polyaxon.processing.data_decoders.TFExampleDecoder(keys_to_features, items_to_handlers)
```

A decoder for TensorFlow Examples.
(A mirror to tf.slim.data TFExampleDecoder)

Decoding Example proto buffers is comprised of two stages: (1) Example parsing
and (2) tensor manipulation.

In the first stage, the tf.parse_example function is called with a list of
FixedLenFeatures and SparseLenFeatures. These instances tell TF how to parse
the example. The output of this stage is a set of tensors.

In the second stage, the resulting tensors are manipulated to provide the
requested 'item' tensors.

To perform this decoding operation, an ExampleDecoder is given a list of
ItemHandlers. Each ItemHandler indicates the set of features for stage 1 and
contains the instructions for post_processing its tensors for stage 2.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_decoders.py#L113)</span>
## SplitTokensDecoder

```python
polyaxon.processing.data_decoders.SplitTokensDecoder(delimiter=' ', tokens_feature_name='tokens', length_feature_name='length', prepend_token=None, append_token=None)
```

A DataDecoder that splits a string tensor into individual tokens and
returns the tokens and the length.
Optionally prepends or appends special tokens.

- __Args__:
	- __delimiter__: Delimiter to split on. Must be a single character.
	- __tokens_feature_name__: A descriptive feature name for the token values
	- __length_feature_name__: A descriptive feature name for the length value


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_decoders.py#L158)</span>
## TFSequenceExampleDecoder

```python
polyaxon.processing.data_decoders.TFSequenceExampleDecoder(context_keys_to_features, sequence_keys_to_features, items_to_handlers)
```

A decoder for TensorFlow Examples.
Decoding Example proto buffers is comprised of two stages: (1) Example parsing
and (2) tensor manipulation.
In the first stage, the tf.parse_example function is called with a list of
FixedLenFeatures and SparseLenFeatures. These instances tell TF how to parse
the example. The output of this stage is a set of tensors.
In the second stage, the resulting tensors are manipulated to provide the
requested 'item' tensors.
To perform this decoding operation, an ExampleDecoder is given a list of
ItemHandlers. Each ItemHandler indicates the set of features for stage 1 and
contains the instructions for post_processing its tensors for stage 2.

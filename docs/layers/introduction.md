# Introduction

All `Layers` in Polyaxon inherits from the `BaseLayer` (which is `GraphModule` child).

This property allows the layers to share the common behaviors.

All layers must defined there behavior in the `_build` function. 
And they should take into account the current mode of the estimator. (`TRAIN`, `EVAL`, and `PREDICT`).

```python
import polyaxon as plx

layer = plx.layers.Dense(units=64, activation='tanh')
```

Once the layer is created, it can be called as many time as needed with different inputs.

The layer itself knows how to validate the incoming values.

A layer can build other layers inside its `_build` function.

## Example

```python
import tensorflow as tf
import polyaxon as plx

rnn_lstm = plx.layers.LSTM(units=3, 
                           activation='tanh', 
                           recurrent_activation='sigmoid', 
                           dropout=0.3)
```

Note that for activations, initializers, and regularizers you can use a string (should be one of the supported values),
you can provide a function, or a tensor/value.

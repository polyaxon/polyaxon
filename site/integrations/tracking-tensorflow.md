---
title: "Tensorflow Tracking"
meta_title: "Tensorflow Tracking"
meta_description: "Polyaxon allows to schedule Tensorflow experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "TensorFlow is a free and open-source software library for dataflow and differentiable programming across a range of tasks. It is a symbolic math library, and is also used for machine learning applications such as neural networks."
image: "../../content/images/integrations/tensorflow.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
featured: false
popularity: 2
visibility: public
status: published
---

Polyaxon allows to schedule Tensorflow experiments and distributed Tensorflow experiments, and supports tracking metrics, outputs, and models.

With Polyaxon you can:

 * log hyperparameters for every run
 * see learning curves for losses and metrics during training
 * see hardware consumption and stdout/stderr output during training
 * log images, charts, and other assets
 * log git commit information
 * log env information
 * log model
 * ...


## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with Tensorflow.

## Setup

In order to use Polyaxon tracking with Tensorflow, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Tensorflow Callback

Polyaxon provides a Tensorflow callback, you can use this callback with your experiment to report metrics automatically

```python
from polyaxon.tracking.contrib.tensorflow import PolyaxonCallback

...
estimator.train(hooks=[PolyaxonCallback(...)])
...
```

## Customizing the callback

Polyaxon's callback can be customized to alter the default behavior:

 * It will use the current initialized run unless you pass a different run
 * You can enable images logging 
 * You can enable histograms logging 
 * You can enable tensors  logging
 
```python
PolyaxonCallback(run=run, log_image=True, log_histo=True, log_tensor=True)
``` 

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom TensorFlow training loops:

```python
from polyaxon import tracking

with tf.GradientTape() as tape:
    # Get the probabilities
    predictions = model(features)
    # Calculate the loss
    loss = loss_func(labels, predictions)

# Log your metrics
tracking.log_metrics(loss=loss.numpy())
```

## Logging the model

To make sure the model is uploaded to your artifacts store, you can pass  `get_outputs_path("model_rel_path", is_dir=True)` to your checkpoint dir:

```python
from polyaxon import tracking
...
tracking.init()
...
model_dir = tracking.get_outputs_path("model", is_dir=True)
classifier = tf.estimator.LinearClassifier(
    model_dir=model_dir,
    feature_columns=[...],
    n_classes=2
)
tracking.log_model_ref(model_dir, framework="tensorflow", ...)
...
classifier.train(input_fn=train_input_fn, steps=100000, hooks=[PolyaxonCallback()])
...
```

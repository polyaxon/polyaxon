---
title: "Hugging Face"
meta_title: "Hugging Face"
meta_description: "Polyaxon allows to schedule experiments based on the hugging-face's transformers library, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "Hugging Face - Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX."
image: "../../content/images/integrations/hugging-face.png"
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

Polyaxon allows to schedule experiments based on hugging-face's transformers library, and supports tracking metrics, outputs, and models.

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

You can use the tracking API to create a custom tracking experience with Keras.

## Setup

In order to use Polyaxon tracking with transformers, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Polyaxon callback

Polyaxon provides a hugging-face callback, you can use this callback with your experiment to report metrics automatically

```python
from polyaxon import tracking
from polyaxon.tracking.contrib.hugging_face import PolyaxonCallback

# ...
tracking.init()
#...
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset if training_args.do_train else None,
    eval_dataset=eval_dataset if training_args.do_eval else None,
    callbacks=[PolyaxonCallback],
    # ...
)
```

## Customizing the callback

If you have a run that is already instanciated, you can pass it directly to the callback:

```python
# ...
callback = PolyaxonCallback(run=run)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset if training_args.do_train else None,
    eval_dataset=eval_dataset if training_args.do_eval else None,
    callbacks=[callback],
    # ...
)
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom Keras training loops:

 * log metrics

```python
tracking.log_mtrics(metric1=value1, metric2=value2, ...)
```

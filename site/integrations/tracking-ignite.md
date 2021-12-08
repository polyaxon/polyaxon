---
title: "Ignite tracking"
meta_title: "Ignite tracking"
meta_description: "Polyaxon allows to schedule Pytorch Ignite experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "Keras is a high-level library to help with training neural networks in PyTorch."
image: "../../content/images/integrations/ignite.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
featured: false
popularity: 1
visibility: public
status: published
---

Polyaxon allows to schedule Ignite experiments, and supports tracking metrics, outputs, and models.

With Polyaxon you can:

 * log hyperparameters for every run
 * see learning curves for losses and metrics during training
 * see hardware consumption and stdout/stderr output during training
 * log images, charts, and other assets
 * log git commit information
 * log env information
 * log model
 * ...

## Overview

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

## Setup

In order to use Polyaxon tracking with Ignite, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Polyaxon logger

```python
from polyaxon.tracking.contrib.ignite import PolyaxonLogger

plx_logger = PolyaxonLogger()
```

## Create a logger

Polyaxon provides a built-in Logger to log params, report metrics, and upload outputs and artifacts automatically.

```python
from polyaxon.tracking.contrib.ignite import PolyaxonLogger

# Create a logger
plx_logger = PolyaxonLogger()
```

## Log params

```python
plx_logger.log_inputs(**{
    "seed": seed,
    "batch_size": batch_size,
    "model": model.__class__.__name__,

    "pytorch version": torch.__version__,
    "ignite version": ignite.__version__,
    "cuda version": torch.version.cuda,
    "device name": torch.cuda.get_device_name(0)
})
```

## Attach logger

Attach the logger to the trainer to log training loss at each iteration

```python
plx_logger.attach_output_handler(
    trainer,
    event_name=Events.ITERATION_COMPLETED,
    tag="training",
    output_transform=lambda loss: {"loss": loss}
)
```

Attach the logger to the evaluator on the training dataset and log NLL,
Accuracy metrics after each epoch.
We setup `global_step_transform=global_step_from_engine(trainer)` to take the epoch
of the `trainer` instead of `train_evaluator`.

```python
plx_logger.attach_output_handler(
    train_evaluator,
    event_name=Events.EPOCH_COMPLETED,
    tag="training",
    metric_names=["nll", "accuracy"],
    global_step_transform=global_step_from_engine(trainer),
)
```

Attach the logger to the evaluator on the validation dataset and log NLL, Accuracy metrics after
each epoch. We setup `global_step_transform=global_step_from_engine(trainer)`
to take the epoch of the `trainer` instead of `evaluator`.

```python
plx_logger.attach_output_handler(
    evaluator,
    event_name=Events.EPOCH_COMPLETED,
    tag="validation",
    metric_names=["nll", "accuracy"],
    global_step_transform=global_step_from_engine(trainer)),
)
```

Attach the logger to the trainer to log optimizer's parameters, e.g. learning rate at each iteration

```python
plx_logger.attach_opt_params_handler(
    trainer,
    event_name=Events.ITERATION_STARTED,
    optimizer=optimizer,
    param_name='lr'  # optional
)
```

## More info

For a complete reference on how to use Ignite's PolyaxonLogger, please visit 
the [Ignite's documentation](https://pytorch.org/ignite/contrib/handlers.html#module-ignite.contrib.handlers.polyaxon_logger).

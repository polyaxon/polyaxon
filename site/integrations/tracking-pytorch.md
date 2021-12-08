---
title: "Pytorch Tracking"
meta_title: "Pytorch Tracking"
meta_description: "Polyaxon allows to schedule Pytorch experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "Pytorch is an open source deep learning framework commonly used for building neural network models. Polyaxon helps with keeping track of model training metadata."
image: "../../content/images/integrations/pytorch.png"
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

Polyaxon allows to schedule Pytorch experiments and distributed Pytorch experiments, and supports tracking metrics, outputs, and models.

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

You can use the tracking API to create a custom tracking experience with Pytorch.

## Setup

In order to use Polyaxon tracking with Pytorch, you need to install Polyaxon library

```bash
pip install polyaxon
```

## Initialize your script with Polyaxon

This is an optional step if you need to perform some manual tracking or to track some information before passing the callback.

```python
from polyaxon import tracking

tracking.init(...)
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom TensorFlow training loops:

 * log metrics

```python
for batch_idx, (data, target) in enumerate(train_loader):
    output = model(data)
    loss = F.nll_loss(output, target)
    loss.backward()
    optimizer.step()
    tracking.log_mtrics(loss=loss)
```

 * log the model
 
```python
asset_path = tracking.get_outputs_path('model.ckpt')
torch.save(model.state_dict(), asset_path)

# log model
tracking.log_artifact_ref(asset_path, framework="pytorch", ...)
```

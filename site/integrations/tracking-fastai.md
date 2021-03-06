---
title: "Fastai Tracking"
meta_title: "Fastai Tracking"
meta_description: "Polyaxon allows to schedule Fastai experiments, and supports tracking metrics, outputs, and models natively."
custom_excerpt: "The fastai library simplifies training fast and accurate neural nets using modern best practices."
image: "../../content/images/integrations/fastai.png"
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

Polyaxon allows to schedule Fastai experiments, and supports tracking metrics, outputs, and models.

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

You can use the tracking API to create a custom tracking experience with Fastai.

## Setup

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

Polyaxon provides a Fastai callback, you can use this callback with your experiment to report metrics automatically.

```python
from polyaxon.tracking.contrib.fastai import PolyaxonCallback

# To log only during one training phase
learn.fit(..., cbs=[PolyaxonCallback()])

# To log continuously for all training phases
learn = learner(..., cbs=[PolyaxonCallback()])
```

## Manual logging

If you want to have more control and use Polyaxon to log metrics in your custom Fastai training loops:

```python
from polyaxon import tracking

# Log your metrics
tracking.log_metrics(metric1=value1, metric2=value2, ...)
```

## Example

In this example we will go through the process of logging a FastAI model using Polyaxon's callback.

This example can be used with the offline mode `POLYAXON_OFFLINE=true` and it does not require a Polyaxon API to run locally. 

To see how this can be turned to a declarative approach to be submitted to a Polyaxon cluster, please check this [example](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/fastai)

```python
import argparse

from fastai.vision.all import *
from fastai.basics import *

# Polyaxon
from polyaxon.tracking.contrib.fastai import PolyaxonCallback

path = untar_data(URLs.MNIST_SAMPLE)
items = get_image_files(path)
tds = Datasets(items, [PILImageBW.create, [parent_label, Categorize()]], splits=GrandparentSplitter()(items))
dls = tds.dataloaders(bs=32, after_item=[ToTensor(), IntToFloatTensor()])

# create a learner with gradient accumulation
learn = cnn_learner(
    dls,
    resnet18,
    loss_func=CrossEntropyLossFlat(),
    cbs=[PolyaxonCallback()]  # Polyaxon
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit', type=int, default=2)
    args = parser.parse_args()
    learn.fit(args.fit)
```

## Fastai V1

If you are using Fastai v1, you will need to import the callback for the v1 version


```python
from polyaxon.tracking.contrib.fastai_v1 import PolyaxonCallback

# Usage as a fit callback
learn.fit_one_cycle(1, 0.02, callbacks=[PolyaxonCallback(learn=learn, monitor='accuracy')])

# Usage as a partial function
Learner(..., callback_fns=partial(PolyaxonFastai, ...), ...)
```

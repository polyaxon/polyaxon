---
title: "Fastai"
meta_title: "Fastai"
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
  - scheduling
featured: false
visibility: public
status: beta
---

Polyaxon allows to schedule Fastai experiments, and supports tracking metrics, outputs, and models.

## Overview

Polyaxon provides a [tracking API](/references/polyaxon-tracking-api/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

## Tracking Fastai experiments

Polyaxon provides a Fastai callback, you can use this callback with your experiment to report metrics automatically

### As a fit callback

```python
from polyaxon_client.tracking import Experiment
from polyaxon_client.tracking.contrib.fastai import Polyaxonfastai

...
experiment = Experiment()
...
learn.fit_one_cycle(1, 0.02, callbacks=[PolyaxonFastai(learn=learn, experiment=experiment, monitor='accuracy')])
```

## As a partial function

```python
from functools import partial

from polyaxon_client.tracking import Experiment
from polyaxon_client.tracking.contrib.fastai import Polyaxonfastai

...
experiment = Experiment()
...
Learner(..., callback_fns=partial(Polyaxonfastai, experiment=experiment, ...), ...)
```

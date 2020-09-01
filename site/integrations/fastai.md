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
featured: false
popularity: 1
visibility: public
status: published
---

Polyaxon allows to schedule Fastai experiments, and supports tracking metrics, outputs, and models.

## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with Fastai.

## Fastai Callback

Polyaxon provides a Fastai callback. You can use this callback with your experiment to report metrics automatically:

### As a fit callback

```python
from polyaxon import tracking
from polyaxon.tracking.contrib.fastai import PolyaxonFastai

...
tracking.init()
...
learn.fit_one_cycle(1, 0.02, callbacks=[PolyaxonFastai(learn=learn, monitor='accuracy')])
```

### As a partial function

```python
from functools import partial

from polyaxon import tracking
from polyaxon.tracking.contrib.fastai import PolyaxonFastai

...
tracking.init()
...
Learner(..., callback_fns=partial(PolyaxonFastai, ...), ...)
```

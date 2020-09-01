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

## Tracking API

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard.

You can use the tracking API to create a custom tracking experience with Tensorflow.

## Tensorflow Callbacks

Polyaxon provides a Tensorflow callback, you can use this callback with your experiment to report metrics automatically

```python
from polyaxon import tracking
from polyaxon.tracking.contrib.tensorflow import LoggingTensorHook, PolyaxonSessionRunHook

...
tracking.init()
...
```

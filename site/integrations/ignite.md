---
title: "Ignite"
meta_title: "Ignite"
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

## Overview

Polyaxon provides a [tracking API](/docs/experimentation/tracking/) to track experiment and report metrics, artifacts, logs, and results to the Polyaxon dashboard,
in addition to this high-level API, you can leverage the built-in Polyaxon Logger provided by the [Ignite library](https://pytorch.org/ignite/contrib/handlers.html#module-ignite.contrib.handlers.polyaxon_logger).

## Setup

In order to use Polyaxon tracking with Ignite, you need to install Polyaxon Client

```bash
pip install polyaxon-client
```

## Usage

Ignite provides a built-in Polyaxon Logger to log params, report metrics, and upload outputs and artifacts automatically.

```python
from ignite.contrib.handlers.polyaxon_logger import *

# Create a logger
plx_logger = PolyaxonLogger()
```

## More info

For a complete reference on how to use Ignite's PolyaxonLogger, please visit the [Ignite's documentation](https://pytorch.org/ignite/contrib/handlers.html#module-ignite.contrib.handlers.polyaxon_logger).

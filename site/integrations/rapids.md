---
title: "Rapids"
meta_title: "Rapids"
meta_description: "Polyaxon allows users to achieve up to 10x speedups in data preprocessing and train models at scale using Rapids."
custom_excerpt: "The RAPIDS suite of open-source software libraries and APIs give you the ability to execute end-to-end data science and analytics pipelines entirely on GPUs. "
image: "../../content/images/integrations/rapids.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - operators
  - distributed-training
  - scheduling
featured: false
popularity: 0
visibility: public
status: examples
---

Polyaxon allows users to achieve up to 10x speedups in data preprocessing and train models at scale using [Rapids](https://rapids.ai).

> **Note**: Users should also look at [CuPy](https://cupy.dev/) which is a NumPy-compatible array library accelerated by CUDA.

## Requirements

To use Polyaxon and RAPIDS to accelerate model training, there are a few requirements:

 * Check the OS and CUDA version [requirements](https://rapids.ai/start.html).
 * Use NVIDIA P100 or later generation GPUs.

## Docker images

Polyaxon schedules containerized workload, which makes creating compatible docker images with Rapids very simple.

### Specifying requirements via conda

```
name: Rapids
channels:
- rapidsai
- nvidia
- conda-forge
dependencies:
- rapids=0.X
```  

Or conda command:

```bash
conda create -n rapids-0.19 -c rapidsai -c nvidia -c conda-forge \
    rapids-blazing=0.19 python=3.7 cudatoolkit=10.2
```

### Using Rapids base docker image

```dockerfile
image: rapidsai/rapidsai:0.19-cuda10.2-runtime-ubuntu18.04-py3.7

...
```

After building and pushing your custom images to a [Docker registry](/docs/setup/connections/registry/), you can run jobs, experiments, or notebooks with the Rapids suite of libraries.

## Using Rapids

 * For data manipulation, users can leverage the [cuDF](https://github.com/rapidsai/cudf) which is a drop-in replacement for [pandas](https://pandas.pydata.org/) for manipulating Dataframe.
 * For feature engineering, [NVTabular](https://github.com/NVIDIA/NVTabular), which sits atop RAPIDS, offers high-level abstractions for feature engineering and building recommenders.
 * For ML algorithms, Rapids offers [cuML](https://docs.rapids.ai/api/cuml/stable/) a GPU-accelerated version of [sklearn](https://scikit-learn.org/stable/)'s algorithms.


By using the Rapids libraries, Polyaxon's users can easily scale their data processing and model development with very few changes to their code. 


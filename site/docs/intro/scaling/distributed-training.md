---
title: "Distributed training"
sub_link: "scaling/distributed-training"
meta_title: "Distributed Training - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Distributed Training - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Scaling with distributed training

Running a distributed job is similar to running a normal job, Polyaxon offers different [distributed runtimes](/docs/experimentation/distributed/).

In this example, we will just show a Tensorflow distributed experiment based on TFJob. But the same principle applies to other supported operators.

```yaml
version: 1.1
kind: component
run:
  kind: tfjob
  chief:
    connections: [my-training-dataset]
    container:
      image: image-with-default-entrypoint
  worker:
    replicas: 2
    environment:
      restartPolicy: OnFailure
    connections: [my-training-dataset]
    container:
      image: image-with-default-entrypoint
      resources:
        limits:
          nvidia.com/gpu: 1
```

This will start a TFJob with 1 replica of type chief and 2 workers.

## Learn More

You can check the [distributed jobs section](/docs/experimentation/distributed/) for more details.

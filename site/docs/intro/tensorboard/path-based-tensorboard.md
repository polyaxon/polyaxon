---
title: "Path-based Tensorboard"
sub_link: "tensorboard/path-based-tensorboard"
meta_title: "Path-based Tensorboard - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Starting Tensorboard based on paths - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - quick-start
sidebar: "intro"
---

## Overview

In the previous Tensorboard tutorials we explored how to start single run and multi-run Tensorboards.

Sometimes you may need to start a Tensorboard that was logged outside of Polyaxon or a Tensorboard that is available on some S3/GCS bucket.

## Path based Tensorboard

Polyaxon provides a couple more Tensorboard versions that expect S3, GCS, Azure, ... These versions will load the path and pass the outputs to a Tensorboard service.

Please check the all versions on the [Tensorboard component hub](https://cloud.polyaxon.com/ui/polyaxon/tensorboard/components) for more details.

Or run the following command:

```bash
polyaxon hub ls -c tensorboard
```

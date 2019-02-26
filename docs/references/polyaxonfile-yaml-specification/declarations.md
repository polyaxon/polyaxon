---
title: "Declarations - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/declarations"
meta_title: "Declarations Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Declarations Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview 

This section is the appropriate place to declare constants and variables
that will be used by the rest of our specification file.

## Example using a simple constant value:

```yaml
declarations:
  batch_size: 128
```

## Example using a list of values or nested values

```yaml
declarations:
  layer_units: [100, 200, 10]
```
Or
```yaml
declarations:
  convolutions:
    conv1:
       kernels: [32, 32]
       size: [2, 2]
       strides: [1, 1]
    conv2:
       kernels: [64, 64]
       size: [2, 2]
       strides: [1, 1]
```

## Explanation

This declaration can be used to pass values to our program:

```yaml
 ... --batch-size={{ batch-size }}
```
Or
```yaml
--unit1="{{ layer_units[0] }}" --unit2="{{ layer_units[1] }}" --unit3="{{ layer_units[2] }}"
```
Or
```yaml
--conv1_kernels="{{ convolutions.conv1.kernels }}" --conv1_stides="{{ convolutions.conv1.strides }}" ...
```

The double-brackets is important and indicate that we want to use our declaration.

The declaration are particularly important for descriptive models.

All your declaration will be exported under the environment variable name `POLYAXON_DECLARATIONS`.

> tip "Polyaxon export your declarations under environment variable name `POLYAXON_DECLARATIONS`"
> Check how you can [get the experiment declarations](/references/polyaxon-tracking-api/experiments/#tracking-experiments-running-inside-polyaxon) to use them with your models.

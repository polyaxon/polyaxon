---
title: "Run - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/run"
meta_title: "Run Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Run Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview

This is where you define how you want to run your code.

 * cmd [required]: The command(s) to run during the execution of your code.
 

## Examples

Some examples of valid `cmd` commands to pass in the polyaxonfile:


```yaml
run:
  cmd: video_prediction_train --num_masks=1
```

Or

```yaml
run:
  cmd: video_prediction_train --num_masks=1 && video_prediction_train --num_masks=2
```

Or

```yaml
run:
  cmd: ./file1.sh || ./file2.sh
```

Or 


```yaml
run:
  cmd: ./file1.sh ; ./file2.sh
```

Or

```yaml
run:
  cmd: 
    - video_prediction_train --num_masks=1
    - video_prediction_train --num_masks=2
    - video_prediction_train --num_masks=3
```

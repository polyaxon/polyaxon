---
title: "Logging - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/logging"
meta_title: "Logging Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Logging Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview

Defines the logging behavior for your execution, this subsection accepts:

 * `level`: The log level.
 * `formatter`: The log formatter regex.


## Example

```yaml
logging:
  level: INFO
```
Or
```yaml
logging:
  level: WARNING
```

---
title: "{{title}}"
meta_title: "{{meta_title}}"
meta_description: "{{meta_description}}"
custom_excerpt: "{{custom_excerpt}}"
code_link: "{{code_link}}"
image: "../../content/images/integrations/{{image}}.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: {{tags}}
featured: {{featured}}
popularity: {{popularity}}
class_name: component
visibility: public
status: published
---

{{meta_description}}

## Component info on Polyaxon Hub

To learn about this component definition or customize its behavior, please check [{{name}} on polyaxon-hub](https://github.com/polyaxon/polyaxon-hub/tree/master/{{name}}).

## Run this component using the CLI

To run the latest version of this component using Polyaxon CLI:

```bash
polyaxon run --hub {{name}} -P ...
```

To use a specific version:


```bash
polyaxon run --hub {{name}}:[tag] -P ...
```

> **Note**: `-P` is for passing parameters, e.g. `-P param1=value1 -P parame2=value2`


## View a running operation on the dashboard

After running an operation with this component, you can view it on the dashboard:

```bash
polyaxon ops dashboard
```

or

```bash
polyaxon ops dashboard -p [project-name] -uid [run-uuid] -y
```

{{service_command}}
## Stop a running operation

To stop a running operation with this component:

```bash
polyaxon ops stop
```

or

```bash
polyaxon ops stop -p [project-name] -uid [run-uuid]
```

## Run this component using the client

To run this component using Polyaxon Client:

```python
from polyaxon.client import RunClient

client = RunClient(...)
client.create_from_hub(component="{{name}}", ...)
```

## Usage in operations

You can also create operations instead of passing params:

```yaml
version: 1.1
kind: operation
params:
  param1: {value: value1}
  ...
hubRef: {{name}}:[tag]
```

## Versions

This component has the following versions: `{{versions}}`

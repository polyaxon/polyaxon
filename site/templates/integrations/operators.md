---
title: "{{title}}"
meta_title: "{{meta_title}}"
meta_description: "{{meta_description}}"
custom_excerpt: "{{custom_excerpt}}"
code_link: "hub/{{name}}.py"
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
class_name: instruction
visibility: public
status: {{status}}
---

{{meta_description}}

## Deploy the {{title}} operator

Before you can use the {{name}} runtime, you need to make sure that {{title}} operator and the CRD (custom resource definition)
are deployed in your cluster.

## Enable the operator

To be able to schedule distributed jobs with the {{title}} operator, you need to enable the operator in your deployment config.

> You need to enable the operator in Polyaxon CE deployment or Polyaxon Agent deployment:

```yaml
operators:
  {{name}}: true
```

## Create a component with the {{name}} runtime

Once you have the {{title}} operator running on a Kubernetes namespace managed by Polyaxon,
you can check the specification for creating components with the {{name}} runtime:

```bash
version: 1.1
kind: component
run:
  kind: {{name}}
  ...
```

For more details about the specification for creating {{name}} runtime, please check please check this
[section](/docs/experimentation/distributed/{{link}}/).

## Run the distributed job


Running components with the {{name}} runtime is similar to running any other component:

```bash
polyaxon run -f manifest.yaml -P ...
```

## View a running operation on the dashboard

After running an operation with this component, you can view it on the Dashboard:

```bash
polyaxon ops dashboard
```

or

```bash
polyaxon ops dashboard -p [project-name] -uid [run-uuid] -y
```

## Stop a running operation

To stop a running operation with this component:

```bash
polyaxon ops stop
```

or

```bash
polyaxon ops stop -p [project-name] -uid [run-uuid]
```

## Run the job using the Python client

To run this component using Polyaxon Client:

```python
from polyaxon.client import RunClient

client = RunClient(...)
client.create_from_polyaxonfile(polyaxonfile="path/to/file", ...)
```

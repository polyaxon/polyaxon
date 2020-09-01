---
title: "Argo"
meta_title: "Argo"
meta_description: "Polyaxon works with Argo to streamline Model Management."
custom_excerpt: "Argo is Container-native Workflow Engine."
image: "../../content/images/integrations/argo.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - automation
  - pipelines
  - scheduling
  - dags
featured: false
popularity: 0
class_name: instruction
visibility: public
status: published
---

You can easily use Polyaxon in your Argo workflows.
Argo is a container-native workflow engine, which means you can use Polyaxon as a step or in multiple steps in an Argo workflow.


## Polyaxon as an Argo step

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
spec:
  entrypoint: polyaxon-job
  templates:
  - name: step1
    ...
  - name: step2
    ...
  - name: polyaxon-job
    container:
      image: polyaxon/polyaxon-cli:1.x.x
      command: ["polyaxon"]
      args: ["run", "-f", "path/to/polyaxonfile.yaml"]
```

> **Tip**: Polyaxon provides a native [DAG](/docs/automation/) runtime for managing your operations dependencies in a simple and efficient way.

---
title: "Services Introduction"
sub_link: "services"
meta_title: "Polyaxon Services - Experimentation"
meta_description: "A Service is the execution of your container with a service."
tags:
    - concepts
    - polyaxon
    - experimentation
    - experiments
    - architecture
sidebar: "experimentation"
---

Services are used to launch Tensorboards, Notebooks, JupyterHub apps, Streamlit/voila/bokeh apps, internal tools, 
and dashboards based on your models and data analysis.

In order to run a service you will need to create a component with a `kind: service` as a runtime:

```yaml
kind: component
version: 1.1
name: notebook
run:
  kind: service
  ports: [8888]
  container:
    image: jupyter/tensorflow-notebook
    command: ["jupyter", "lab"]
    args: [
      "--no-browser",
      "--ip=0.0.0.0",
      "--port={{globals.ports[0]}}",
      "--allow-root",
      "--NotebookApp.allow_origin=*",
      "--NotebookApp.trust_xheaders=True",
      "--NotebookApp.token=",
      "--NotebookApp.base_url={{globals.base_url}}",
      "--LabApp.base_url={{globals.base_url}}"
    ]
```

Same example in Python.

```python
from polyaxon.polyflow import V1Component, V1Service
from polyaxon.k8s import k8s_schemas

service = V1Service(
    ports=[8888],
    container=k8s_schemas.V1Container(
        image="jupyter/tensorflow-notebook",
        command=["jupyter", "lab"],
        args=[
            "--no-browser",
            "--ip=0.0.0.0",
            "--port={{globals.ports[0]}}",
            "--allow-root",
            "--NotebookApp.allow_origin=*",
            "--NotebookApp.trust_xheaders=True",
            "--NotebookApp.token=",
            "--NotebookApp.base_url={{globals.base_url}}",
            "--LabApp.base_url={{globals.base_url}}"
        ]
    ),
)

component = V1Component(name="notebook", run=service)
``` 

### Specification

Please check the [service specification](/docs/experimentation/services/specification/) guide to learn about all details for running services in Polyaxon.

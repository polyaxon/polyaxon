---
title: "Airflow"
meta_title: "Airflow"
meta_description: "Polyaxon provides an Airflow plugin for creating builds, jobs, and experiments."
custom_excerpt: "Airflow is a platform to programmatically author, schedule and monitor workflows."
image: "../../content/images/integrations/airflow.png"
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

Polyaxon provides a rich [Python library](/docs/core/python-library/polyaxon-client/) that can be used with
scheduling tools such as Airflow to submit jobs to Polyaxon.

## Creating a custom operator

In order to use Polyaxon with airflow you just need to create a custom Airflow operator.

Here's a simple operator that will submit a job and can wait for the job to finish based on a flag.

```python
import os

from airflow.models import BaseOperator
from polyaxon.client import RunClient


class PolyaxonOperator(BaseOperator):
    ui_color = "#2ea44f"
    ui_fgcolor = "#fff"

    def __init__(
        self,
        project_name=None,
        polyaxonfile=None,
        watch=False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.polyaxonfile = polyaxonfile
        self.watch = watch
        self.project_name = project_name or os.environ.get("POLYAXON_PROJECT_NAME")

    def execute(self, context):
        client = RunClient(project=self.project_name)
        client.create_from_polyaxonfile(polyaxonfile=self.polyaxonfile)
        if self.watch:
            client.wait_for_condition()
            self.log.info(f"Last status: {client.run_data.status}")
```

> **Tip**: Polyaxon provides a native [DAG](/docs/automation/) runtime for managing your operations and their dependencies in a simple and efficient way.

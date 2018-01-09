Polyaxon helper is a lightweight python library to report metrics and communicate information with Polyaxon.


## Install

```bash
$ pip install -U polyaxon-helper
```


## Getting env variables defined by Polyaxon

Polyaxon defines some variables related to your experiment in environment variables, namely:

 * `POLYAXON_CLUSTER` : defines the cluster definition, e.g.
    ```json
    {
        "master": ["plxjob-master0-8eefb7a1146f476ca66e3bee9b88c1de:2000"],
        "worker": ["plxjob-worker1-8eefb7a1146f476ca66e3bee9b88c1de:2000", "plxjob-worker2-8eefb7a1146f476ca66e3bee9b88c1de:2000"]
    }
    ```
 * `POLYAXON_DECLARATIONS` : defines all the declarations of you polyaxonfile as well as the values from hyperparameters search.
 * `POLYAXON_EXPERIMENT_INFO` : defines information about job, experiment, group, project.
 * `POLYAXON_OUTPUTS_PATH`: defines the outputs path you should use to export your model, tensorboard metrics, ...
 * `POLYAXON_LOG_LEVEL`: The log level if defined in the polyaxonfile.

Of course you can get these values on your own, e.g. in python:

```python
import os

os.getenv('POLYAXON_CLUSTER', None)
```

however we recommend using our helper library, so that your code and models will be backward compatible to future changes of the platform.

```python
from polyaxon_helper import (
    get_cluster_def,
    get_declarations,
    get_experiment_info,
    get_outputs_path,
    get_log_level
)

cluster_def = get_cluster_def()
declarations = get_declarations()
experiment_info = get_experiment_info()
outputs_path = get_outputs_path()
log_level = get_log_level()
```


## Reporting metrics to Polyaxon

In order to report metrics for an experiment, just add these line in you program.

```python
from polyaxon_helper import send_metrics

send_metrics(accuracy=0.9, precision=0.95)
```

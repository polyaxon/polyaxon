---
title: "Tracking on other environments"
sub_link: "polyaxon-tracking-api/other-environments"
meta_title: "Tracking experiments on other environments - Polyaxon References"
meta_description: "Tracking experiments running outside a cluster managed by Polyaxon."
visibility: public
status: published
tags:
    - tracking
    - reference
    - polyaxon
    - client
    - sdk
    - experiment
sidebar: "polyaxon-tracking-api"
---

This guide will help track experiments running outside a cluster managed by Polyaxon, e.g. laptop, spark, sagemaker, colab, ...

## Authenticating Polyaxon tracking

In order to use Polyaxon Tracking API, the user must provide an authenticated client. There are several options to do that, 
you can look at the Polyaxon Python Client reference to learn how you can [authenticate a client](/references/polyaxon-client-python/#authentication).

Once you have an authenticated client, you can pass it to your experiment or group:

```python
from polyaxon_client.client import PolyaxonClient

client = PolyaxonClient(host='HOST_IP',
                        token='4ee4e5e6080a196d11f637b950fce1587b29ef36')
                        
experiment = Experiment(client=client)
```

## Creating new experiments

In order to create an experiment, the user must provide a project, that she has access to, where the experiment will be added: 

```python
# An experiment in a project that belongs to the authenticated user 
experiment = Experiment(client=client, project='quick-start')

# Or an experiment in a project that belongs to another user 
# The authenticated user must have access rights to the project 
experiment = Experiment(client=client, project='user2/t2t')
```

You can also add an experiment to a group:

```python
# An experiment in a project that belongs to the authenticated user 
experiment = Experiment(client=client, project='quick-start', group_id=GROUP_ID)
```

Now you can create the experiment:

```python
experiment.create()
```

You can also provide several more information during the creation:

```python
experiment.create(
    name=None, 
    framework=None, 
    backend=None, 
    tags=None,
    description=None,
    config=None,
    base_outputs_path=None)
```

Several information can be set or updated later, e.g. name, description, framework, etc, see [reference](/references/polyaxon-tracking-api/experiments/) for more information.

## Retrieving and updating an experiment

In order to retrieve an experiment to either update it or resume it:

```python
# An experiment in a project that belongs to the authenticated user 
experiment = Experiment(client=client, project='quick-start', experiment_id=EXPERIMENT_ID)

# Or an experiment in a project that belongs to another user 
# The authenticated user must have access rights to the project 
experiment = Experiment(client=client, project='user2/t2t', experiment_id=EXPERIMENT_ID)
```

And then fetch the experiment data:

```python
experiment.get_entity_data()
```

You can now call other methods to update certain fields, see [reference](/references/polyaxon-tracking-api/experiments/) for more information.

## Logging

In order to upload logs to Polyaxon API when running an external experiment, users have 2 choices:

 * using the python logging module
 * uploading logs manually
 
### Logging module

If you use the logging module in your experiment, any log with level INFO or above will be tracked by Polyaxon:

```python
logger = logging.getLogger()
...
logger.info('Train model...')
``` 

This method will not impact your experiments, since it will use an async thread to send logs periodically.

### Uploading logs manually

You can also opt to send logs manually, for example at the end of the experiment:

```python
experiment = Experiment(client=client, track_logs=False)
experiment.send_logs(logs)
```

## Hyperparams tuning

If you wish to track several experiments produced by a Hyperparams tuning module, e.g. HyperOpt, you can create first a group, and add all your experiments under that group:

```python

description = 'Conducting hyperaprams with HyperOpt'
tags = ['optimization']

group = Group(client=client, project="quick-start")
group.create(name='external-group', description=description=description, tags=tags)


for experiment_params in OPTIMIZATION_MODULE.get_suggestion():
    experiment = group.create_experiment(description=description, framework='scikit-learn', tags=tags)
    experiment.log_params(**experiment_params)
    ...
    experiment.log_succeeded()
group.log_succeeded()
```

N.B. You can create groups or use previously created group to just include your experiments for organizational purposes. 
In such case you can either retrieve the group first or pass the group id to experiment.

## Example


```python
import argparse
import logging

# Polyaxon
from polyaxon_client.tracking import Experiment

from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

logger = logging.getLogger()


def model(log_learning_rate, max_depth=3, num_rounds=10, min_child_weight=5):
    model = XGBClassifier(
        learning_rate=10 ** log_learning_rate,
        max_depth=max_depth,
        num_rounds=num_rounds,
        min_child_weight=min_child_weight,
        objective='binary:logistic',
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    return accuracy_score(pred, y_test)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log_learning_rate',
        type=int,
        default=-3
    )
    parser.add_argument(
        '--max_depth',
        type=int,
        default=3
    )
    parser.add_argument(
        '--num_rounds',
        type=int,
        default=10
    )
    parser.add_argument(
        '--min_child_weight',
        type=int,
        default=5
    )
    args = parser.parse_args()

    # Polyaxon
    experiment = Experiment('iris')
    experiment.create(framework='xgboost', tags=['examples'])
    experiment.log_params(log_learning_rate=args.log_learning_rate,
                          max_depth=args.max_depth,
                          num_rounds=args.num_rounds,
                          min_child_weight=args.min_child_weight)

    iris = load_iris()
    X = iris.data
    Y = iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    # Polyaxon
    experiment.log_data_ref(data=X_train, data_name='x_train')
    experiment.log_data_ref(data=y_train, data_name='y_train')
    experiment.log_data_ref(data=X_test, data_name='X_test')
    experiment.log_data_ref(data=y_test, data_name='y_train')

    logger.info('Train model...')
    accuracy = model(log_learning_rate=args.log_learning_rate,
                     max_depth=args.max_depth,
                     num_rounds=args.num_rounds,
                     min_child_weight=args.min_child_weight)
    experiment.log_metrics(accuracy=accuracy)
```

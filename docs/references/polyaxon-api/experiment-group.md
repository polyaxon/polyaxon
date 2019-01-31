---
title: "Polyaxon Experiment Group Rest API"
sub_link: "polyaxon-api/experiment-group"
meta_title: "Polyaxon Experiment Group Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Experiment Group Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - experiment
    - experiment-group
    - orchestration
    - hyperparameters
    - tuning
    - optimization
sidebar: "polyaxon-api"
---

## Get experiment group

<span class="api api-get">
/api/v1/{username}/{project_name}/groups/{id}/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}}/ \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

### Example response

```json
{
    "id": 2,
    "uuid": "9b073653a6ee446fabc9f420541bb2d2",
    "name": null,
    "unique_name": "root.quick-start.2",
    "user": "root",
    "description": null,
    "last_status": "succeeded",
    "project": "root.quick-start",
    "created_at": "2018-08-19T22:37:47.820000+02:00",
    "updated_at": "2018-08-19T22:55:13.877000+02:00",
    "started_at": "2018-08-19T22:37:49.778000+02:00",
    "finished_at": "2018-08-19T22:55:13.877000+02:00",
    "tags": null,
    "concurrency": 5,
    "search_algorithm": "random",
    "current_iteration": 0,
    "content": "{'version': 1, 'kind': 'group', 'hptuning': {'concurrency': 5, 'random_search': {'n_experiments': 10}, 'matrix': {'learning_rate': {'linspace': '0.001:0.1:5'}, 'dropout': {'values': [0.25, 0.3]}, 'activation': {'values': ['relu', 'sigmoid']}}}, 'declarations': {'batch_size': 128, 'num_steps': 500, 'num_epochs': 1}, 'build': {'image': 'tensorflow/tensorflow:1.4.1-py3', 'build_steps': ['pip3 install --no-cache-dir -U polyaxon-client']}, 'run': {'cmd': 'python3 model.py --batch_size={{ batch_size }} \\\\ --num_steps={{ num_steps }} \\\\ --learning_rate={{ learning_rate }} \\\\ --dropout={{ dropout }} \\\\ --num_epochs={{ num_epochs }} \\\\ --activation={{ activation }}'}}",
    "hptuning": {
        "early_stopping": null,
        "concurrency": 5,
        "seed": null,
        "matrix": {
            "dropout": {
                "values": [
                    0.25,
                    0.3
                ]
            },
            "activation": {
                "values": [
                    "relu",
                    "sigmoid"
                ]
            },
            "learning_rate": {
                "linspace": {
                    "num": 5,
                    "stop": 0.1,
                    "start": 0.001
                }
            }
        },
        "random_search": {
            "n_experiments": 10
        }
    },
    "has_tensorboard": null,
    "num_experiments": 10,
    "num_pending_experiments": 0,
    "num_running_experiments": 0,
    "num_scheduled_experiments": 0,
    "num_succeeded_experiments": 10,
    "num_failed_experiments": 0,
    "num_stopped_experiments": 0,
    "bookmarked": false
}
```

## Update experiment group

<span class="api api-patch">
/api/v1/{username}/{project_name}/groups/{id}/
</span>

<b>Example curl request</b>

```
curl -X PATCH \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}} \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "new description"
}'
```

<b>Example response</b>

```json
{
    "id": 2,
    "uuid": "9b073653a6ee446fabc9f420541bb2d2",
    "name": null,
    "unique_name": "root.quick-start.2",
    "user": "root",
    "description": "new description",
    "last_status": "succeeded",
    "project": "root.quick-start",
    "created_at": "2018-08-19T22:37:47.820000+02:00",
    "updated_at": "2018-08-23T12:07:59.437479+02:00",
    "started_at": "2018-08-19T22:37:49.778000+02:00",
    "finished_at": "2018-08-19T22:55:13.877000+02:00",
    "tags": null,
    "concurrency": 5,
    "search_algorithm": "random",
    "current_iteration": 0,
    "content": "{'version': 1, 'kind': 'group', 'hptuning': {'concurrency': 5, 'random_search': {'n_experiments': 10}, 'matrix': {'learning_rate': {'linspace': '0.001:0.1:5'}, 'dropout': {'values': [0.25, 0.3]}, 'activation': {'values': ['relu', 'sigmoid']}}}, 'declarations': {'batch_size': 128, 'num_steps': 500, 'num_epochs': 1}, 'build': {'image': 'tensorflow/tensorflow:1.4.1-py3', 'build_steps': ['pip3 install --no-cache-dir -U polyaxon-client']}, 'run': {'cmd': 'python3 model.py --batch_size={{ batch_size }} \\\\ --num_steps={{ num_steps }} \\\\ --learning_rate={{ learning_rate }} \\\\ --dropout={{ dropout }} \\\\ --num_epochs={{ num_epochs }} \\\\ --activation={{ activation }}'}}",
    "hptuning": {
        "early_stopping": null,
        "concurrency": 5,
        "seed": null,
        "matrix": {
            "dropout": {
                "values": [
                    0.25,
                    0.3
                ]
            },
            "activation": {
                "values": [
                    "relu",
                    "sigmoid"
                ]
            },
            "learning_rate": {
                "linspace": {
                    "num": 5,
                    "stop": 0.1,
                    "start": 0.001
                }
            }
        },
        "random_search": {
            "n_experiments": 10
        }
    },
    "has_tensorboard": null,
    "num_experiments": 10,
    "num_pending_experiments": 0,
    "num_running_experiments": 0,
    "num_scheduled_experiments": 0,
    "num_succeeded_experiments": 10,
    "num_failed_experiments": 0,
    "num_stopped_experiments": 0,
    "bookmarked": false
}
```


## Delete experiment group

<span class="api api-delete">
/api/v1/{username}/{project_name}/groups/{id}/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://localhost:8000/api/v1/root/quick-start/groups/1 \
  -H 'Authorization: token {{token}}'
```

## Stop experiment group

<span class="api api-post">
/api/v1/{username}/{project_name}/groups/{id}/stop
</span>

<b>Example curl request</b>


```
curl -X POST \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}}/stop \
  -H 'Authorization: token {{token}}'
```


## Start experiment group tensorboard

<span class="api api-post">
/api/v1/{username}/{project_name}/groups/{id}/tensorboard/start
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}}/tensorboard/start \
  -H 'Authorization: token {{token}}'
```

## Stop experiment group tensorboard

<span class="api api-post">
/api/v1/{username}/{project_name}/groups/{id}/stop
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}}/tensorboard/stop \
  -H 'Authorization: token {{token}}'
```


## Get group statuses

<span class="api api-get">
/api/v1/{username}/{project_name}/groups/{id}/statuses
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/root/quick-start/groups/{{id}}/statuses \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

<b>Example response</b>

```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "uuid": "a5540894189a4b018c38cf5048c57f13",
            "created_at": "2018-08-19T22:37:47.822000+02:00",
            "message": null,
            "status": "created",
            "experiment_group": 2
        },
        {
            "id": 2,
            "uuid": "6c81259a1072401987f60a7c057eecd1",
            "created_at": "2018-08-19T22:37:49.775000+02:00",
            "message": null,
            "status": "running",
            "experiment_group": 2
        },
        {
            "id": 3,
            "uuid": "67036254d49e4f668802342b9a8e0f18",
            "created_at": "2018-08-19T22:55:13.874000+02:00",
            "message": null,
            "status": "succeeded",
            "experiment_group": 2
        }
    ]
}
```

## Bookmark group

<span class="api api-post">
/api/v1/{username}/{project_name}/groups/{id}/bookmark/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/groups/{{id}}/bookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

## Unbookmark experiment group


<span class="api api-delete">
/api/v1/{username}/{project_name}/groups/{id}/unbookmark/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/groups/{{id}}/unbookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

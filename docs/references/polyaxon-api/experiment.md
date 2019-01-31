---
title: "Polyaxon Experiment Rest API"
sub_link: "polyaxon-api/experiment"
meta_title: "Polyaxon Experiment Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Experiment Rest API Specification."
visibility: public
status: published
tags:
    - api
    - polyaxon
    - reference
    - rest
    - experiment
    - experiment-job
    - orchestration
sidebar: "polyaxon-api"
---

## Get experiment

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{id}/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
  "id": 1,
  "uuid": "d26f9c63ee9b492885c8c679e3ca06ff",
  "name": null,
  "unique_name": "root.quick-start.1",
  "user": "root",
  "description": null,
  "created_at": "2018-08-22T21:25:05.764283+02:00",
  "updated_at": "2018-08-22T21:27:54.669279+02:00",
  "started_at": "2018-08-22T21:26:36.583432+02:00",
  "finished_at": "2018-08-22T21:27:54.669115+02:00",
  "last_status": "succeeded",
  "original": null,
  "project": "root.quick-start",
  "experiment_group": null,
  "build_job": "root.quick-start.builds.1",
  "tags": null,
  "config": {
    "build": {
      "image": "tensorflow/tensorflow:1.4.1-py3",
      "build_steps": [
        "pip3 install --no-cache-dir -U polyaxon-client"
      ]
    },
    "version": 1,
    "kind": "experiment",
    "run": {
      "cmd": "python3 model.py"
    }
  },
  "declarations": null,
  "resources": null,
  "last_metric": {
    "loss": 0.0502114,
    "precision": 0.9986705,
    "accuracy": 0.9827
  },
  "num_jobs": 1,
  "is_clone": false,
  "has_tensorboard": null,
  "bookmarked": false
}
```

## Update experiment

<span class="api api-patch">
/api/v1/{username}/{project_name}/experiments/{id}/
</span>

<b>Example curl request</b>

```
curl --request PATCH \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "description": "new description"
}'
```

<b>Example response</b>

```json
{
  "id": 1,
  "uuid": "d26f9c63ee9b492885c8c679e3ca06ff",
  "name": null,
  "unique_name": "root.quick-start.1",
  "user": "root",
  "description": "new description",
  "created_at": "2018-08-22T21:25:05.764283+02:00",
  "updated_at": "2018-08-22T21:32:10.408021+02:00",
  "started_at": "2018-08-22T21:26:36.583432+02:00",
  "finished_at": "2018-08-22T21:27:54.669115+02:00",
  "last_status": "succeeded",
  "original": null,
  "project": "root.quick-start",
  "experiment_group": null,
  "build_job": "root.quick-start.builds.1",
  "tags": null,
  "config": {
    "build": {
      "image": "tensorflow/tensorflow:1.4.1-py3",
      "build_steps": [
        "pip3 install --no-cache-dir -U polyaxon-client"
      ]
    },
    "version": 1,
    "kind": "experiment",
    "run": {
      "cmd": "python3 model.py"
    }
  },
  "declarations": null,
  "resources": null,
  "last_metric": {
    "loss": 0.0502114,
    "precision": 0.9986705,
    "accuracy": 0.9827
  },
  "num_jobs": 1,
  "is_clone": false,
  "has_tensorboard": null,
  "bookmarked": false
}
```

## Delete experiment

<span class="api api-delete">
/api/v1/{username}/{project_name}/experiments/{id}/
</span>


<b>Example curl request</b>

```
curl --request DELETE \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}' \
  --header 'Authorization: token {{token}}'
```


## Restart experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/restart/
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/restart' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
  "id": 3,
  "uuid": "0a63969440a446699aa082e654a94010",
  "name": null,
  "unique_name": "root.quick-start.3",
  "user": "root",
  "description": "new description",
  "created_at": "2018-08-22T21:35:16.560243+02:00",
  "updated_at": "2018-08-22T21:35:16.562301+02:00",
  "started_at": null,
  "finished_at": null,
  "last_status": "created",
  "original": "root.quick-start.1",
  "project": "root.quick-start",
  "experiment_group": null,
  "build_job": null,
  "tags": null
}
```

## Resume experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/resume/
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/resume' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
  "id": 3,
  "uuid": "0a63969440a446699aa082e654a94010",
  "name": null,
  "unique_name": "root.quick-start.3",
  "user": "root",
  "description": "new description",
  "created_at": "2018-08-22T21:35:16.560243+02:00",
  "updated_at": "2018-08-22T21:35:16.562301+02:00",
  "started_at": null,
  "finished_at": null,
  "last_status": "created",
  "original": "root.quick-start.1",
  "project": "root.quick-start",
  "experiment_group": null,
  "build_job": null,
  "tags": null
}
```

## Copy experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/copy
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/resume' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
  "id": 3,
  "uuid": "0a63969440a446699aa082e654a94010",
  "name": null,
  "unique_name": "root.quick-start.3",
  "user": "root",
  "description": "new description",
  "created_at": "2018-08-22T21:35:16.560243+02:00",
  "updated_at": "2018-08-22T21:35:16.562301+02:00",
  "started_at": null,
  "finished_at": null,
  "last_status": "created",
  "original": "root.quick-start.1",
  "project": "root.quick-start",
  "experiment_group": null,
  "build_job": null,
  "tags": null
}
```

## Stop experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/stop
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/stop' \
  --header 'Authorization: token {{token}}'
```

## Get experiment statuses

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{id}/statuses
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{id}}/statuses' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "uuid": "0cc6f8c7622842b09be0878d9d4a8089",
            "created_at": "2018-08-22T21:25:05.767070+02:00",
            "message": null,
            "status": "created",
            "experiment": 1
        },
        {
            "id": 2,
            "uuid": "656a889d42104fc2b46685a15dcdfa1c",
            "created_at": "2018-08-22T21:25:07.646364+02:00",
            "message": null,
            "status": "building",
            "experiment": 1
        },
        {
            "id": 3,
            "uuid": "51fadf52068a4dd19598dd3d6b70b897",
            "created_at": "2018-08-22T21:26:33.768065+02:00",
            "message": null,
            "status": "scheduled",
            "experiment": 1
        },
        {
            "id": 4,
            "uuid": "63715940647f44efbb7260bef766e33e",
            "created_at": "2018-08-22T21:26:36.581108+02:00",
            "message": null,
            "status": "starting",
            "experiment": 1
        },
        {
            "id": 5,
            "uuid": "e6cb3da1cbbb4b9e919169ddaec03e50",
            "created_at": "2018-08-22T21:26:46.587029+02:00",
            "message": null,
            "status": "running",
            "experiment": 1
        },
        {
            "id": 6,
            "uuid": "2261fd8b4c8a44fdb24411c9e29b0632",
            "created_at": "2018-08-22T21:27:54.666729+02:00",
            "message": null,
            "status": "succeeded",
            "experiment": 1
        }
    ]
}
```

## Get experiment metrics

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{id}/metrics
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/metrics' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "created_at": "2018-08-22T21:27:52.732286+02:00",
            "values": {
                "loss": 0.050211381167173386,
                "precision": 0.9986705183982849,
                "accuracy": 0.982699990272522
            },
            "experiment": 1
        },
        {
            "id": 2,
            "created_at": "2018-08-22T21:32:29.765700+02:00",
            "values": {
                "precision": 0.9,
                "accuracy": 0.85
            },
            "experiment": 1
        }
    ]
}
```

## Create experiment metric

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/metrics
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/metrics' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
	"values": {"precision": 0.9, "accuracy": 0.85}
}'
```

<b>Example response</b>

```json
{
    "id": 6,
    "created_at": "2018-08-22T23:15:30.637932+02:00",
    "values": {
        "precision": 0.9,
        "accuracy": 0.85
    },
    "experiment": 1
}
```


## List experiment jobs

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{id}/jobs
</span>


<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/jobs' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json

  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "uuid": "41429e2b877447769ebc78be6a6b1c2b",
      "unique_name": "root.quick-start.1.1.master",
      "role": "master",
      "experiment": 1,
      "last_status": "succeeded",
      "created_at": "2018-08-22T21:26:33.862708+02:00",
      "updated_at": "2018-08-22T21:27:53.234997+02:00",
      "started_at": "2018-08-22T21:26:39.594738+02:00",
      "finished_at": "2018-08-22T21:27:53.234843+02:00",
      "resources": null,
      "node_scheduled": "gke-cluster-1-default-pool-001a34db-h8nj"
    }
  ]
}
```

## Get experiment logs

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{id}/logs/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/logs' \
  --header 'Authorization: token {{token}}'
```

## Start experiment tensorboard

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/tensorboard/start
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/metrics' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
	"values": {"precision": 0.9, "accuracy": 0.85}
}'
```

## Stop experiment tensorboard

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{id}/tensorboard/stop
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/tensorboard/start' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
	"values": {"precision": 0.9, "accuracy": 0.85}
}'
```

## Download experiment outputs

<span class="api api-get">
 /api/v1/{username}/{project_name}/experiments/{id}/outputs
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}/outputs' \
  --header 'Authorization: token {{token}}'
```


## Get experiment job

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{experiment_id}/jobs/{id}/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}//jobs/{{job_id}}' \
  --header 'Authorization: token {{token}}'
```

## Get experiment job statuses

<span class="api api-get">
/api/v1/{username}/{project_name}/experiments/{experiment_id}/jobs/{id}/statuses/
</span>


<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//experiments/{{experiment_id}}//jobs/{{job_id}}/statuses' \
  --header 'Authorization: token {{token}}'
```


## Bookmark experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/{experiment_id}/bookmark/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{experiment_id}}/bookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
```

## Unbookmark experiment


<span class="api api-delete">
/api/v1/{username}/{project_name}/experiments/{experiment_id}/unbookmark/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments/{{experiment_id}}/unbookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
```

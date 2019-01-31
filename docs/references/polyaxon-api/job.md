---
title: "Polyaxon Job Rest API"
sub_link: "polyaxon-api/job"
meta_title: "Polyaxon Job Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Job Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - job
    - orchestration
sidebar: "polyaxon-api"
---

## Get job

<span class="api api-get">
/api/v1/{username}/{project_name}/jobs/{id}/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "id": 1,
    "uuid": "75b316b21d0d4f2c8acae4f3106c3ad7",
    "name": null,
    "unique_name": "root.quick-start.jobs.1",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:15.734000+02:00",
    "updated_at": "2018-08-19T22:40:48.514000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:17.993000+02:00",
    "finished_at": "2018-08-19T22:40:48.513000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2",
    "is_clone": false,
    "original": null,
    "config": {
        "run": {
            "cmd": "python3 -u download_data.py"
        },
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "job"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "bookmarked": false
}
```

## Update job

<span class="api api-patch">
/api/v1/{username}/{project_name}/jobs/{id}/
</span>

<b>Example curl request</b>

```
curl --request PATCH \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/' \
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
    "uuid": "75b316b21d0d4f2c8acae4f3106c3ad7",
    "name": null,
    "unique_name": "root.quick-start.jobs.1",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:15.734000+02:00",
    "updated_at": "2018-08-19T22:40:48.514000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:17.993000+02:00",
    "finished_at": "2018-08-19T22:40:48.513000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2",
    "is_clone": false,
    "original": null,
    "config": {
        "run": {
            "cmd": "python3 -u download_data.py"
        },
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "job"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "bookmarked": false
}
```

## Delete job

<span class="api api-delete">
/api/v1/{username}/{project_name}/jobs/{id}/
</span>


<b>Example curl request</b>

```
curl --request DELETE \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}' \
  --header 'Authorization: token {{token}}'
```

## Get job statuses

<span class="api api-get">
/api/v1/{username}/{project_name}/jobs/{id}/statuses/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/statuses' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "uuid": "30f1b847f71744ac8521fa7b8232f73e",
            "created_at": "2018-08-19T22:40:15.737000+02:00",
            "message": null,
            "status": "created",
            "details": null,
            "job": 1
        },
        {
            "id": 3,
            "uuid": "69ad44abdd6f4b6d8faadb334383da28",
            "created_at": "2018-08-19T22:40:17.990000+02:00",
            "message": null,
            "status": "scheduled",
            "details": null,
            "job": 1
        },
        {
            "id": 4,
            "uuid": "23fc3bb5f00b4bf196b544d616681c4b",
            "created_at": "2018-08-19T22:40:18.153000+02:00",
            "message": "PodInitializing",
            "status": "building",
            "job": 1
        },
        {
            "id": 11,
            "uuid": "f2fba809e7b144128dbba91955a682c8",
            "created_at": "2018-08-19T22:40:22.939000+02:00",
            "message": null,
            "status": "running",
            "job": 1
        },
        {
            "id": 17,
            "uuid": "31c6a6cf30d2479b828d0c8cba5a57ee",
            "created_at": "2018-08-19T22:40:48.510000+02:00",
            "message": "Completed",
            "status": "succeeded",
            "job": 1
        }
    ]
}
```

## Restart job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/{id}/restart
</span>

<b>Example curl request</b>

```json
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/restart' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>


```json
{
    "id": 1,
    "uuid": "75b316b21d0d4f2c8acae4f3106c3ad7",
    "name": null,
    "unique_name": "root.quick-start.jobs.2",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:15.734000+02:00",
    "updated_at": "2018-08-19T22:40:48.514000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:17.993000+02:00",
    "finished_at": "2018-08-19T22:40:48.513000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2",
    "is_clone": false,
    "original": "root.quick-start.jobs.1",
    "config": {
        "run": {
            "cmd": "python3 -u download_data.py"
        },
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "job"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "bookmarked": false
}
```

## Resume job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/{id}/resume
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/resume' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>


```json
{
    "id": 1,
    "uuid": "75b316b21d0d4f2c8acae4f3106c3ad7",
    "name": null,
    "unique_name": "root.quick-start.jobs.2",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:15.734000+02:00",
    "updated_at": "2018-08-19T22:40:48.514000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:17.993000+02:00",
    "finished_at": "2018-08-19T22:40:48.513000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2",
    "is_clone": false,
    "original": "root.quick-start.jobs.1",
    "config": {
        "run": {
            "cmd": "python3 -u download_data.py"
        },
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "job"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "bookmarked": false
}
```

## Copy job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/{id}/resume
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/copy' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>



```json
{
    "id": 1,
    "uuid": "75b316b21d0d4f2c8acae4f3106c3ad7",
    "name": null,
    "unique_name": "root.quick-start.jobs.2",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:15.734000+02:00",
    "updated_at": "2018-08-19T22:40:48.514000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:17.993000+02:00",
    "finished_at": "2018-08-19T22:40:48.513000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2",
    "is_clone": false,
    "original": "root.quick-start.jobs.1",
    "config": {
        "run": {
            "cmd": "python3 -u download_data.py"
        },
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "job"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "bookmarked": false
}
```

## Stop job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/{id}/stop
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/stop' \
  --header 'Authorization: token {{token}}'
```

## Get job logs

<span class="api api-get">
/api/v1/{username}/{project_name}/jobs/{id}/logs
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//jobs/{{id}}/logs' \
  --header 'Authorization: token {{token}}'
```

## Download job outputs

<span class="api api-get">
/api/v1/{username}/{project_name}/jobs/{id}/outputs
</span>


<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//jobs/{{id}}/outputs' \
  --header 'Authorization: token {{token}}'
```

## Bookmark job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/{id}/bookmark/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/bookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
```

## Unbookmark job


<span class="api api-delete">
/api/v1/{username}/{project_name}/jobs/{job_id}/unbookmark/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs/{{id}}/unbookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
```

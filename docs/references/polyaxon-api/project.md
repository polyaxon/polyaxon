---
title: "Polyaxon Project Rest API"
sub_link: "polyaxon-api/project"
meta_title: "Polyaxon Project Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Project Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - project
    - orchestration
sidebar: "polyaxon-api"
---

## List projects for user

<span class="api api-get">
/api/v1/{username}/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}' \
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
            "id": 6,
            "uuid": "34b36cd393de462ba2dd27c1af69f010",
            "user": "root",
            "name": "foo",
            "unique_name": "root.foo",
            "description": "foo",
            "tags": null,
            "created_at": "2018-08-23T00:30:18.674062+02:00",
            "updated_at": "2018-08-23T00:30:18.674123+02:00",
            "is_public": true
        },
        {
            "id": 5,
            "uuid": "77596423f3174d898daa21774d0df144",
            "user": "root",
            "name": "quick-start",
            "unique_name": "root.quick-start",
            "description": null,
            "tags": null,
            "created_at": "2018-08-19T22:06:28.974000+02:00",
            "updated_at": "2018-08-19T22:06:28.974000+02:00",
            "is_public": true
        }
    ]
}
```

## Get project

<span class="api api-get">
 /api/v1/{username}/{project_name}/
</span>


<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "id": 5,
    "uuid": "77596423f3174d898daa21774d0df144",
    "user": "root",
    "name": "quick-start",
    "unique_name": "root.quick-start",
    "description": null,
    "tags": null,
    "created_at": "2018-08-19T22:06:28.974000+02:00",
    "updated_at": "2018-08-19T22:06:28.974000+02:00",
    "is_public": true,
    "has_code": true,
    "has_tensorboard": null,
    "has_notebook": null,
    "num_experiment_groups": 1,
    "num_independent_experiments": 4,
    "num_experiments": 14,
    "num_jobs": 5,
    "num_builds": 2,
    "bookmarked": false
}
```

## Create project

<span class="api api-post">
/api/v1/projects/
</span>


<b>Body</b>

param | type | optional
------|------|----------
name | string | False
description | string | True
is_public | bool | True
tags | list<string> | True

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/projects' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
	"name": "foo"
}'
```

<b>Example response</b>

```json
{
    "id": 6,
    "uuid": "34b36cd393de462ba2dd27c1af69f010",
    "user": "root",
    "name": "bal",
    "unique_name": "root.foo",
    "description": "foo",
    "tags": null,
    "created_at": "2018-08-23T00:30:18.674062+02:00",
    "updated_at": "2018-08-23T00:30:18.674123+02:00",
    "is_public": true
}
```


## Update project

<span class="api api-patch">
/api/v1/{username}/{project}/
</span>


<b>Example curl request</b>

```
curl --request PATCH \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}' \
  --header 'Authorization: token {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "description": "new description"
}'
```

<b>Example response</b>

```json
{
    "id": 5,
    "uuid": "77596423f3174d898daa21774d0df144",
    "user": "root",
    "name": "quick-start",
    "unique_name": "root.quick-start",
    "description": "new description",
    "tags": null,
    "created_at": "2018-08-19T22:06:28.974000+02:00",
    "updated_at": "2018-08-23T00:35:34.511744+02:00",
    "is_public": true,
    "has_code": true,
    "has_tensorboard": null,
    "has_notebook": null,
    "num_experiment_groups": 1,
    "num_independent_experiments": 4,
    "num_experiments": 14,
    "num_jobs": 5,
    "num_builds": 2,
    "bookmarked": false
}
```

## Delete project

<span class="api api-delete">
/api/v1/{username}/{project_name}/
</span>

<b>Example curl request</b>

```
curl --request DELETE \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}' \
  --header 'Authorization: token {{token}}'
```

## Upload repo for a project

<span class="api api-put">
/api/v1/{username}/{project_name}/repo/upload/
</span>

## Download repo for a project

<span class="api api-get">
/api/v1/{username}/{project_name}/repo/download/
</span>

## List experiment groups

<span class="api api-get">
/api/v1/{username}/{project_name}/groups/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/root/quick-start/groups \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

<b>Example response</b>

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
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
            "search_algorithm": "random"
        }
    ]
}
```

## Create experiment groups

<span class="api api-post">
/api/v1/{username}/{project_name}/groups/
</span>


<b>Example curl request</b>

```
curl -X POST \
  http://localhost:8000/api/v1/root/quick-start/groups \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"name": "group-1", "description": "my group", "content": "..."}'
```

<b>Example response</b>

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
    "search_algorithm": "random"
}
```

## List experiments

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/
</span>>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "count": 14,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 20,
            "uuid": "76446631463048b99a54832aff771d27",
            "name": null,
            "unique_name": "root.quick-start.20",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T23:05:51.476000+02:00",
            "updated_at": "2018-08-19T23:06:13.001000+02:00",
            "started_at": "2018-08-19T23:05:53.894000+02:00",
            "finished_at": "2018-08-19T23:06:13.001000+02:00",
            "last_status": "stopped",
            "original": null,
            "project": "root.quick-start",
            "experiment_group": null,
            "build_job": "root.quick-start.builds.2",
            "tags": null
        },
        {
            "id": 9,
            "uuid": "19b8373bd8bb4fd59eae423f36581edd",
            "name": null,
            "unique_name": "root.quick-start.9",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T22:14:48.438000+02:00",
            "updated_at": "2018-08-19T22:56:25.960000+02:00",
            "started_at": "2018-08-19T22:14:50.775000+02:00",
            "finished_at": "2018-08-19T22:56:25.960000+02:00",
            "last_status": "succeeded",
            "original": null,
            "project": "root.quick-start",
            "experiment_group": null,
            "build_job": "root.quick-start.builds.2",
            "tags": null
        },
    ...
    ]
}
```

## Create experiment

<span class="api api-post">
/api/v1/{username}/{project_name}/experiments/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments \
  -H 'Authorization: token {{token}}' \
  -H 'Content-Type: application/json' \
  -d '{"name": "experiment-1", "description": "my experiment", "config": "..."}'
```

<b>Example response</b>

```JSON
{
    "id": 21,
    "user": "new",
    "name": "new-1",
    "description": "my new experiment",
    "original_experiment": null,
    "config": null,
    "declarations": null,
    "tags": null
}
```

## List Jobs

<span class="api api-get">
/api/v1/{username}/{project_name}/jobs/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/jobs \
  -H 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "uuid": "18723bfd0ae74dc3a17ade6e1e09bca8",
            "name": null,
            "unique_name": "root.quick-start.jobs.5",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T23:03:45.923000+02:00",
            "updated_at": "2018-08-19T23:03:54.810000+02:00",
            "last_status": "succeeded",
            "started_at": "2018-08-19T23:03:48.640000+02:00",
            "finished_at": "2018-08-19T23:03:54.809000+02:00",
            "tags": null,
            "project": "root.quick-start",
            "build_job": "root.quick-start.builds.2"
        },
        {
            "id": 3,
            "uuid": "fddc44c052474561bbc8dc2061884a46",
            "name": null,
            "unique_name": "root.quick-start.jobs.3",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T22:40:19.946000+02:00",
            "updated_at": "2018-08-19T22:41:33.500000+02:00",
            "last_status": "succeeded",
            "started_at": "2018-08-19T22:40:21.963000+02:00",
            "finished_at": "2018-08-19T22:41:33.500000+02:00",
            "tags": null,
            "project": "root.quick-start",
            "build_job": "root.quick-start.builds.2"
        },
        ...
    ]
}
```

## Create Job

<span class="api api-post">
/api/v1/{username}/{project_name}/jobs/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/experiments \
  -H 'Authorization: token {{token}}' \
  -H 'Content-Type: application/json' \
  -d '{"name": "job-1", "description": "my job", "config": "..."}'
```

<b>Example response</b>


```json
{
    "id": 2,
    "uuid": "0ee55633fdd34aa6a063e086abda6569",
    "name": null,
    "unique_name": "root.quick-start.jobs.2",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:40:17.843000+02:00",
    "updated_at": "2018-08-19T22:40:40.372000+02:00",
    "last_status": "succeeded",
    "started_at": "2018-08-19T22:40:20.051000+02:00",
    "finished_at": "2018-08-19T22:40:40.372000+02:00",
    "tags": null,
    "project": "root.quick-start",
    "build_job": "root.quick-start.builds.2"
}
```

## List Builds

<span class="api api-get">
/api/v1/{username}/{project_name}/builds/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
```

<b>Example response</b>

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "uuid": "86a84a6aaf0d4f298433a8aee8b615de",
            "name": null,
            "unique_name": "root.quick-start.builds.2",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T22:14:42.607000+02:00",
            "updated_at": "2018-08-19T22:14:48.870000+02:00",
            "started_at": "2018-08-19T22:14:42.646000+02:00",
            "finished_at": "2018-08-19T22:14:48.870000+02:00",
            "last_status": "succeeded",
            "tags": null,
            "project": "root.quick-start"
        },
        {
            "id": 1,
            "uuid": "f97fdb5e430640d3adcbad033a065433",
            "name": null,
            "unique_name": "root.quick-start.builds.1",
            "user": "root",
            "description": null,
            "created_at": "2018-08-19T22:06:35.963000+02:00",
            "updated_at": "2018-08-19T22:09:34.637000+02:00",
            "started_at": "2018-08-19T22:06:36.031000+02:00",
            "finished_at": "2018-08-19T22:09:34.637000+02:00",
            "last_status": "succeeded",
            "tags": null,
            "project": "root.quick-start"
        }
    ]
}
```

## Create Build

<span class="api api-post">
/api/v1/{username}/{project_name}/builds/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"name": "build-1", "description": "my build", "config": "..."}'
```

<b>Example response</b>

```json
{
    "id": 2,
    "uuid": "86a84a6aaf0d4f298433a8aee8b615de",
    "name": null,
    "unique_name": "root.quick-start.builds.2",
    "user": "root",
    "description": null,
    "created_at": "2018-08-19T22:14:42.607000+02:00",
    "updated_at": "2018-08-19T22:14:48.870000+02:00",
    "started_at": "2018-08-19T22:14:42.646000+02:00",
    "finished_at": "2018-08-19T22:14:48.870000+02:00",
    "last_status": "succeeded",
    "tags": null,
    "project": "root.quick-start"
}
```

## List tensorboards

<span class="api api-get">
/api/v1/{username}/{project_name}/tensorboards/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/tensorboards \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```


## Start project tensorboard

<span class="api api-pot">
/api/v1/{username}/{project_name}/tensorboard/start/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/tensorboard/start \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

## Stop project tensorboard

<span class="api api-post">
/api/v1/{username}/{project_name}/tensorboard/stop/
</span>


<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/tensorboard/stop \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```


## Start notebook

<span class="api api-post">
/api/v1/{username}/{project_name}/notebook/start/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/notebook/start \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```


## Stop notebook

<span class="api api-post">
/api/v1/{username}/{project_name}/notebook/stop/
</span>


<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/notebook/stop \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
```

## Bookmark project

<span class="api api-post">
/api/v1/{username}/{project_name}/bookmark/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/bookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

## Unbookmark project


<span class="api api-delete">
/api/v1/{username}/{project_name}/unbookmark/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/unbookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache'
```

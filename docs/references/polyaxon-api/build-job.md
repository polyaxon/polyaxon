---
title: "Polyaxon Build Rest API"
sub_link: "polyaxon-api/build-job"
meta_title: "Polyaxon Build Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Build Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - build
    - job
    - container
    - docker
sidebar: "polyaxon-api"
---

## Get build

<span class="api api-get">
/api/v1/{username}/{project_name}/builds/{id}/
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/1' \
  --header 'Authorization: token {{token}}'
```

<b>Example response</b>

```json
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
    "project": "root.quick-start",
    "config": {
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "build"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "num_jobs": 0,
    "num_experiments": 1,
    "dockerfile": "\nFROM tensorflow/tensorflow:1.4.1-py3\n\nENV LC_ALL en_US.UTF-8\nENV LANG en_US.UTF-8\nENV LANGUAGE en_US.UTF-8\n# Use bash as default shell, rather than sh\nENV SHELL /bin/bash\n\nWORKDIR /code\n\nRUN pip3 install --no-cache-dir -U polyaxon-client\nCOPY build /code\n",
    "commit": "2f758b8902d4cf5d4147b09706613ec108eda369",
    "bookmarked": false
}
```

## Update build

<span class="api api-patch">
/api/v1/{username}/{project_name}/builds/{id}/
</span>

<b>Example curl request</b>

```
curl --request PATCH \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/1/' \
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
    "project": "root.quick-start",
    "config": {
        "build": {
            "build_steps": [
                "pip3 install --no-cache-dir -U polyaxon-client"
            ],
            "image": "tensorflow/tensorflow:1.4.1-py3"
        },
        "version": 1,
        "kind": "build"
    },
    "resources": null,
    "node_scheduled": "gke-cluster-1-default-pool-65d093c7-7hk4",
    "num_jobs": 0,
    "num_experiments": 1,
    "dockerfile": "\nFROM tensorflow/tensorflow:1.4.1-py3\n\nENV LC_ALL en_US.UTF-8\nENV LANG en_US.UTF-8\nENV LANGUAGE en_US.UTF-8\n# Use bash as default shell, rather than sh\nENV SHELL /bin/bash\n\nWORKDIR /code\n\nRUN pip3 install --no-cache-dir -U polyaxon-client\nCOPY build /code\n",
    "commit": "2f758b8902d4cf5d4147b09706613ec108eda369",
    "bookmarked": false
}
```

## Delete build

<span class="api api-delete">
/api/v1/{username}/{project_name}/builds/{id}/
</span>

<b>Example curl request</b>

```
curl --request DELETE \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/{{id}}' \
  --header 'Authorization: token {{token}}'
```

## Get build statuses

<span class="api api-get">
/api/v1/{username}/{project_name}/builds/{id}/statuses
</span>

<b>Example curl request</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/{{id}}/statuses' \
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


## Stop build

<span class="api api-post">
/api/v1/{username}/{project_name}/builds/{id}/
</span>

<b>Example curl request</b>

```
curl --request POST \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/{{id}}/stop' \
  --header 'Authorization: token {{token}}'
```

## Get build logs

<span class="api api-get">
/api/v1/{username}/{project_name}/builds/{id}/logs
</span>

<b>Example curl request</b>

  * Authorization: Token "token"

<b>Example response</b>

```
curl --request GET \
  --url 'http://{{base_api_url}}/api/v1/{{username}}/{{project}}//builds/{{id}}/logs' \
  --header 'Authorization: token {{token}}'
```


## Bookmark build

<span class="api api-post">
/api/v1/{username}/{project_name}/builds/{id}/bookmark/
</span>

<b>Example curl request</b>

```
curl -X POST \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/{{id}}/bookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
```

## Unbookmark build


<span class="api api-delete">
/api/v1/{username}/{project_name}/builds/{id}/unbookmark/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  http://{{base_api_url}}/api/v1/{{username}}/{{project}}/builds/{{id}}/unbookmark \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
```

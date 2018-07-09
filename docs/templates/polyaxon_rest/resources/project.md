## Create a project

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/projects/
```

### Body

param | type | optional
______|______|____________
name | string | False
description | string | True
is_public | bool | True
tags | list<string> | True

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## List projects for user

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Get a project details

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Update a project details

### Method

<span class="api api-patch">PATCH</span>

### Url

```
PATCH /api/v1/{username}/{project_name}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Delete a project

### Method

<span class="api api-delete">DELETE</span>

### Url

```
DELETE /api/v1/{username}/{project_name}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 204 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Upload repo for a project

### Method

<span class="api api-put">PUT</span>

### Url

```
PUT /api/v1/{username}/{project_name}/repo/upload/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Download repo for a project

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/repo/download/
```

### Headers

  * Authorization: Token "token"


### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## List experiment groups

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/groups/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Create experiment groups

### Method

<span class="api api-post">POST</span>

### Url

```
GET /api/v1/{username}/{project_name}/groups/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## List experiments

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Create experiment

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## List Jobs

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/jobs/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Create Job

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/jobs/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## List Builds

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/builds/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Create Build

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/builds/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## List tensorboards

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/tensorboards/
```

### Headers

  * Authorization: Token "token"


### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Start project tensorboard

### Method

<span class="api api-pot">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/tensorboard/start/
```

### Headers

  * Authorization: Token "token"


### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Stop project tensorboard

### Method

<span class="api api-post">POST</span>

### Url

```
GET /api/v1/{username}/{project_name}/tensorboard/stop/
```

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

### Headers

  * Authorization: Token "token"

## Start notebook

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/notebook/start/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Stop notebook

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/notebook/stop/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

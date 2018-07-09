## Get experiment

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Update experiment

<span class="api api-patch">PATCH</span>

### Url

```
PATCH /api/v1/{username}/{project_name}/experiments/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Delete experiment

<span class="api api-delete">DELETE</span>

### Url

```
DELETE /api/v1/{username}/{project_name}/experiments/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get experiment metrics

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/{id}/metrics
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Create experiment metric

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/metrics
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 201 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## List experiment jobs


<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/{id}/jobs
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Restart experiment

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/restart/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Resume experiment

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/resume/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Copy experiment

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/copy
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Stop experiment

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/stop
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get experiment logs

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/{id}/logs/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Start experiment tensorboard

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/tensorboard/start
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Stop experiment tensorboard

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/experiments/{id}/tensorboard/stop
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Download experiment outputs

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/experiments/{id}/outputs
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


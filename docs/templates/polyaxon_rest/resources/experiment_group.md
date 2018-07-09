## Get experiment group

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/groups/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## List experiment group experiments

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/groups/{id}/experiments
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Update experiment group

### Method

<span class="api api-get">PATCH</span>

### Url

```
PATCH /api/v1/{username}/{project_name}/groups/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Delete experiment group

### Method

<span class="api api-get">DELETE</span>

### Url

```
DELETE /api/v1/{username}/{project_name}/groups/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 204 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Stop experiment group

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/groups/{id}/stop
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Start experiment group tensorboard

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/groups/{id}/tensorboard/start
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Stop experiment group tensorboard

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/groups/{id}/stop
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Get group statuses

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/groups/{id}/statuses
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

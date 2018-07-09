## Get build

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/builds/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Update build

<span class="api api-patch">PATCH</span>

### Url

```
PATCH /api/v1/{username}/{project_name}/builds/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Delete build

<span class="api api-delete">DELETE</span>

### Url

```
DELETE /api/v1/{username}/{project_name}/builds/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get build statuses

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/builds/{id}/statuses
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get build status details

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/builds/{build_id}/statuses/{id}
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Stop build

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/builds/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get build logs

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/builds/{id}/logs
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

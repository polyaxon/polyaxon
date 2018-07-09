## Get job

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/jobs/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Update job

### Method

<span class="api api-get">PATCH</span>

### Url

```
PATCH /api/v1/{username}/{project_name}/jobs/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Delete job

### Method

<span class="api api-get">DELETE</span>

### Url

```
DELETE /api/v1/{username}/{project_name}/jobs/{id}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Get job statuses

### Method

<span class="api api-get">GET</span>

### Url

```
GEt /api/v1/{username}/{project_name}/jobs/{id}/statuses/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Restart job

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/jobs/{id}/restart
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Resume job

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/jobs/{id}/resume
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Copy job

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/jobs/{id}/resume
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Stop job

### Method

<span class="api api-get">POST</span>

### Url

```
POST /api/v1/{username}/{project_name}/jobs/{id}/stop
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Get job logs

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/jobs/{id}/logs
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Download job outputs

### Method

<span class="api api-get">GET</span>

### Url

```
GET /api/v1/{username}/{project_name}/jobs/{id}/downloads
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

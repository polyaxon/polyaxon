## Login user and return user's token

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/users/token/
```

### Body

param | type | optional
------|------|------------
username | string | False
password | string | False

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Activate user

### Method

<span class="api api-post">POST</span>

### Url

```
DELETE /api/v1/users/activate/{username}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

## Delete user

### Method

<span class="api api-delete">DELETE</span>

### Url

```
DELETE /api/v1/users/delete/{username}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 204 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)


## Grant a user the superuser role

### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/superusers/grant/{username}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)



## Revoke the superuser role from user


### Method

<span class="api api-post">POST</span>

### Url

```
POST /api/v1/superusers/revoke/{username}/
```

### Headers

  * Authorization: Token "token"

### Responses

 * Response 200 (application/json)
 * Response 400 (application/json)
 * Response 401 (application/json)
 * Response 403 (application/json)
 * Response 404 (application/json)

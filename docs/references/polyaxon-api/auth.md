---
title: "Polyaxon Auth Rest API"
sub_link: "polyaxon-api/auth"
meta_title: "Polyaxon Auth Rest API Specification - Polyaxon References"
meta_description: "Polyaxon Auth Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - auth
    - login
    - logout
sidebar: "polyaxon-api"
---

## Login user and return user's token

<span class="api api-post">
/api/v1/users/token/
</span>

<b>Body</b>

param | type | optional
------|------|------------
username | string | False
password | string | False


<b>Example curl request</b>

```
curl -X POST \
  http://localhost:8000/api/v1/users/token \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"username": "admin", "password": "admin"}'
```

<b>Example response</b>

```json
{
    "token": "8ff04973157b2a5831329fbb1befd37f93e4de4f"
}
```

## Get user info


<span class="api api-get">
/api/v1/users/
</span>

<b>Example curl request</b>

```
curl -X GET \
  http://localhost:8000/api/v1/users \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
```

<b>Example response</b>

```json
{
    "username": "root",
    "email": "root@polyaxon.local",
    "is_superuser": true
}
```

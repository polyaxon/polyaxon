---
title: "Polyaxon User Rest API"
sub_link: "polyaxon-api/user"
meta_title: "Polyaxon User Rest API Specification - Polyaxon References"
meta_description: "Polyaxon User Rest API Specification."
visibility: public
status: published
tags:
    - api
    - reference
    - polyaxon
    - rest
    - user
    - management
    - roles
    - permissions
sidebar: "polyaxon-api"
---

## Activate user

<span class="api api-post">
/api/v1/users/activate/{username}/
</span>

<b>Example curl request</b>

```
curl -X POST \
  'http://localhost:8000/api/v1/users/activate/{{user}}' \
  -H 'Authorization: token {{token}}'
```

## Delete user

<span class="api api-delete">
/api/v1/users/delete/{username}/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  'http://localhost:8000/api/v1/users/delete/{{user}}' \
  -H 'Authorization: token {{token}}' \
  -H 'Cache-Control: no-cache' \
```


## Grant a user the superuser role

<span class="api api-post">
/api/v1/superusers/grant/{username}/
</span>

<b>Example curl request</b>

```
curl -X POST \
  'http://localhost:8000/api/v1/superusers/grant/{{user}}' \
  -H 'Authorization: token {{token}}'
```


## Revoke the superuser role from user


<span class="api api-post">
/api/v1/superusers/revoke/{username}/
</span>

<b>Example curl request</b>

```
curl -X DELETE \
  'http://localhost:8000/api/v1/superusers/grant/{{user}}' \
  -H 'Authorization: token {{token}}'
```

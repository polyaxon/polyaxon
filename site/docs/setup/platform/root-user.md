---
title: "Root user"
sub_link: "platform/root-user"
meta_title: "Root user and db access in Polyaxon - Configuration"
meta_description: "Polyaxon's root user and db access."
tags:
  - configuration
  - polyaxon
  - kubernetes
sidebar: "setup"
---

## Root user

The default superuser/root user for polyaxon.
You can set a password or a random password will be generated that you can retrieve later.

```yaml
user:
  username: "rootuser"
  email: "rootuser@polyaxon.local"
  password: "rootpassword"
```

## Admin view

To enable the DB admin interface:

```yaml
ui:
  adminEnabled: true
```

The user/password generated will be used for access the admin interface.

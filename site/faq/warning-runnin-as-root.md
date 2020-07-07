---
title: "Logs show warning in containers: running as root"
meta_title: "Logs show warning in containers: running as root - FAQ"
meta_description: "By default all containers are running with root user, but you can set a security context to change this behaviour."
featured: false
custom_excerpt: "By default all containers are running with root user, but you can set a security context to change this behaviour."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - api
---

By default all containers are running with root user, but you can set a security context to change this behaviour.

If you are seeing message like:

> *** WARNING: you are running uWSGI as root !!! (use the --uid flag) ***

> Running a worker with superuser privileges when the

You can change this behaviour by setting a security context.

 * Enable security context with default configuration:

```yaml
securityContext:
  enabled: true
```


 * Enable security context with custom configuration:

```yaml
securityContext:
  enabled: false
  user: 1111
  group: 1111
```

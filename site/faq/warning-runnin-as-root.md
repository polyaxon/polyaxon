---
title: "Logs show warning in containers: running as root"
meta_title: "Logs show warning in containers: running as root - FAQ"
meta_description: "By default, all containers are running with root user, but you can set a security context to change this behavior."
featured: false
custom_excerpt: "By default, all containers are running with root user, but you can set a security context to change this behavior."
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

By default, all containers are running with root user, but you can set a security context to change this behavior.

If you are seeing a message like:

<blockquote class="info">
 * you are running uWSGI as root !!! (use the --uid flag)
<br/>
 * Running a worker with superuser privileges
</blockquote>

You can change this behavior by setting a [security context](/docs/setup/platform/common-reference/#security-context).

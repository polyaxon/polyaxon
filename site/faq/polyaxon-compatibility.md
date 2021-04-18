---
title: "What is Polyaxon compatibility check?"
meta_title: "What is Polyaxon compatibility check? - FAQ"
meta_description: "Polyaxon will periodically communicate with a remote compatibility server to check compatibility version."
featured: false
custom_excerpt: "Polyaxon will periodically communicate with a remote compatibility server to check compatibility version."
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

Polyaxon will periodically communicate with a remote compatibility server.
This is utilized for a couple of things, primarily:

 * Check the compatibility version API
 * Getting information about the current version of Polyaxon
 * Retrieving important system notices

The following information is reported:

 * A unique installation ID
 * The version of Polyaxon deployed

With that said, you can disable the compatibility check with the following setting:

```yaml
intervals:
  compatibilityCheck: -1
```

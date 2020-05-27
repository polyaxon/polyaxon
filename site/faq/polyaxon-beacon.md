---
title: "What is Polyaxon Beacon?"
meta_title: "What is Polyaxon Beacon? - FAQ"
meta_description: "Polyaxon will periodically communicate with a remote beacon server to report anonymous usage data."
featured: false
custom_excerpt: "Polyaxon will periodically communicate with a remote beacon server to report anonymous usage data."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - beacon
---

Polyaxon will periodically communicate with a remote beacon server.
This is utilized for a couple of things, primarily:

 * Getting information about the current version of Polyaxon
 * Retrieving important system notices

The following information is reported:

 * A unique installation ID
 * The version of Polyaxon
 * General anonymous statistics on the data pattern (such as errors, installation type, ...)

The data reported is minimal and it greatly helps the development team behind Polyaxon.
With that said, you can disable the beacon with the following setting:

```yaml
trackerBackend: "noop"
```

---
title: "My builds fail in EKS cluster"
meta_title: "My builds fail in EKS cluster - FAQ"
meta_description: "If your builds are failing while using the native builder because of internet/dns resolution issues."
featured: false
custom_excerpt: "If your builds are failing while using the native builder because of internet/dns resolution issues."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - containers
  - scheduling
---

If your builds are failing while using the native builder because of internet/dns resolution issues in an EKS cluster,
similar to this [issue](https://github.com/polyaxon/polyaxon/issues/442),
you should be aware that the latest versions of the AWS EKS-optimized AMI disable the docker bridge network by default.
To fix this issue please see the note on the native builder [integration page](/integrations/dockerizer/).

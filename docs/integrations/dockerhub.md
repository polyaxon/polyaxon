---
title: "Docker Hub"
meta_title: "Docker Hub Registry"
meta_description: "How to pull images from your private docker hub registry."
custom_excerpt: "Docker Hub is a service provided by Docker for finding and sharing container images with your team. Docker Hub is the world's largest library and community for container images"
image: "../../content/images/integrations/dockerhub.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registry
featured: false
visibility: public
status: published
---

You can use your docker images hosted on [https://hub.docker.com/](https://hub.docker.com/).


## Overview

You can use your public images without the need to set any configuration. In order to use private docker images hosted on docker hub, you need to set access credentials. 

## Add credentials to use with docker hub

You can use the `privateRegistries` section to set your docker hub credentials:

```yaml
privateRegistries:
  - "my_username:my_password@https://index.docker.io/v1/"
```

or 

```yaml
privateRegistries:
  - host: "https://index.docker.io/v1/"
    user: "myname"
    password: "mypassword"
```

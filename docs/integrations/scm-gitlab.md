---
title: "Repos on GitLab"
meta_title: "GitLab"
meta_description: "How to use code from GitLab repositories on Polyaxon. You can use code from your GitLab repositories directly in Polyaxon projects without having to check them out on your local machine first."
custom_excerpt: "GitLab is a single application for the entire software development lifecycle. From project planning and source code management to CI/CD, monitoring, and security."
image: "../../content/images/integrations/gitlab.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - scm
  - repos
featured: true
visibility: public
status: published
---

## Overview

Polyaxon supports repos hosted on GitLab. 
You can use code from your GitLab repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private GitLab repos, you don't need to have a GitLab account
to use code from public GitLab repositories. e.g. `https://gitlab.com/polyaxon/polyaxon-quick-start`

```yaml
build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache -U polyaxon-client
  ref: 4b798d5663e336bc6a5e1021bd84174e0303ef4a
```

## Open GitLab Developer Settings
Open Access Tokens

![gitlab-integration1](../../content/images/integrations/gitlab/img1.png)

## Generate a new token

Choose a name for the token (e.g. "Polyaxon"), 
then grant the token API permissions to be able to use full integration 
features or select read_repository and read_user to only have ability to use existing repositories. 
This will enable Polyaxon to read your repositories and detect new commits. 
Click the Generate Token button at the bottom to create the token.

![gitlab-integration2](../../content/images/integrations/gitlab/img2.png)

Or If you only want to allow Polyaxon read access please select:

![gitlab-integration3](../../content/images/integrations/gitlab/img3.png)

## Copy the token

Select the token and copy it.

## Update your deployment config file

```yaml
reposAccessToken: TokenHashHere
```

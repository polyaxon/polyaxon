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
featured: false
popularity: 0
visibility: public
status: published
---

You can use code from your GitLab repositories directly in Polyaxon projects without having to check them out on your local machine first.

## Overview

Polyaxon supports repos hosted on GitLab (cloud and on-premise). 
You can use code from your GitLab repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private GitLab repos, you don't need to have a GitLab account
to use code from public GitLab repositories.

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

## Create a secret

```yaml
kubectl -n polyaxon create secret generic github-connection-1 --from-literal=POLYAXON_GIT_CREDENTIALS="TokenHash"
```

## Add th repos you want to use to the connections catalog

```yaml
connections:
  - name: repo1
    kind: git
    schema:
      url: https://github.com/org/repo1
    secret:
      name: "github-connection-1"
  - name: repo2
    kind: git
    schema:
      url: https://github.com/org/repo2
    secret:
      name: "github-connection-1"
  - name: repo3
    kind: git
    schema:
      url: https://github.com/org/repo3
    secret:
      name: "other-connection"
```

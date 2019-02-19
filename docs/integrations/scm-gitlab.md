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

Polyaxon supports repos hosted on GitLab (cloud and on-premise). 
You can use code from your GitLab repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private GitLab repos, you don't need to have a GitLab account
to use code from public GitLab repositories.

## Setting an external repo for code tracking

You need a project on polyaxon that it's not linked to a code repo yet:

```bash
polyaxon project create --name=project1
```

And then you need set the git url:

```bash
polyaxon project -p project1 git --url="https://gitlab.com/org/repo-name"
```

If the project is private you need to add `--private` to the command to indicate that the repo is private, i.e.

```bash
polyaxon project -p project1 git --url="https://gitlab.com/org/repo-name" --private
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

## Update your deployment config file and deploy/upgrade

```yaml
reposAccessToken: TokenHashHere
```

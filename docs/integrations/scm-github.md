---
title: "Repos on Github"
meta_description: "How to use code from GitHub repositories on Polyaxon."
custom_excerpt: "You can use code from your GitHub repositories directly in Polyaxon projects without 
having to check them out on your local machine first."
image: "../../content/images/integrations/github.png"
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

Polyaxon supports repos hosted on GitHub. 
You can use code from your GitHub repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private GitHub repos, you don't need to have a GitHub account
to use code from public GitHub repositories. e.g.

```yaml
build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache -U polyaxon-client
  git: https://github.com/polyaxon/polyaxon-quick-start
  ref: 4b798d5663e336bc6a5e1021bd84174e0303ef4a
```

## Open GitHub Developer Settings
At the bottom of the settings menu on the left, click Developer Settings.

![github-integration1](../../content/images/integrations/github/img1.png)

## Choose personal access token
Select the Personal access tokens link on the left. On that page, click the Generate new token button on the right.

![github-integration1](../../content/images/integrations/github/img2.png)

## Generate a new token

Choose a name for the token (e.g. "Polyaxon"), 
then grant the token "repo" and "admin:repo_hook" permissions. 
This will enable Polyaxon to read your repositories and detect new commits. 
Click the Generate Token button at the bottom to create the token.

![github-integration1](../../content/images/integrations/github/img3.png)

## Copy the token

Select the token and copy it. Alternatively, 
you can click the blue icon next to the token to automatically copy it to the clipboard.

![github-integration1](../../content/images/integrations/github/img4.png)


## Update your deployment config file

```yaml
reposAccessToken: TokenHashHere
```

---
title: "External Repos"
sub_link: "external-repos"
meta_title: "Integrate your workflow with github, gitlab, bitbucket in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use external git providers for code management."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - environment
    - orchestration
    - github
    - gitlab
    - bitbucket
sidebar: "configuration"
---

Polyaxon allows to use external git providers for code management. 
Currently only github/gitlab/bitbucket are supported for private external repos. 

## External public repos

To start experiments and jobs using external public repos, the users need to update their polyaxonfiles' build section with git url, e.g.

```yaml
build:
  image: ubuntu
  git: https://github.com/user/repo
```  

This will just tell Polyaxon to create a build based on latest master.

To be able to use a specific commit/branch/other treeish, you should add a `ref`:

```yaml
build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip3 install --no-cache -U polyaxon-client
  git: https://github.com/polyaxon/polyaxon-quick-start
  ref: 4b798d5663e336bc6a5e1021bd84174e0303ef4a
```


## External private repos

In order to use code from private repos, you must add an access token to allow Polyaxon to pull the repo, 
both [gitlab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) and [github](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) provide a way to create access tokens.

Depending on your provider, you should create an access token and allow the `repos` access, and then you need to update your deployment `config.yaml`

```yaml
reposAccessToken: TokenHashHere
``` 

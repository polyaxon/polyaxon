---
title: "Repos on Bitbucket"
meta_title: "Bitbucket"
meta_description: "How to use code from Bitbucket repositories on Polyaxon. You can use code from your Bitbucket repositories directly in Polyaxon projects without having to check them out on your local machine first."
custom_excerpt: "Bitbucket is Git repository management solution designed for professional teams. It gives you a central place to manage git repositories, collaborate on your source code and guide you through the development flow."
image: "../../content/images/integrations/bitbucket.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - scm
  - repos
featured: false
visibility: public
status: published
---

## Overview

Polyaxon supports repos hosted on Bitbucket (cloud and on-premise). 
You can use code from your Bitbucket repositories directly in Polyaxon projects without 
having to check them out on your local machine first. 

N.B. Polyaxon supports public and private Bitbucket repos, you don't need to have a Bitbucket account
to use code from public Bitbucket repositories.

## Setting an external repo for code tracking

You need a project on polyaxon that it's not linked to a code repo yet:

```bash
polyaxon project create --name=project1
```

And then you need set the git url:

```bash
polyaxon project -p project1 git --url="https://bitbucket.com/org/repo-name"
```

If the project is private you need to add `--private` to the command to indicate that the repo is private, i.e.

```bash
polyaxon project -p project1 git --url="https://bitbucket.com/org/repo-name" --private
```

## Access token

Bitbucket allows to create [app passwords](https://confluence.atlassian.com/bitbucket/app-passwords-828781300.html), 
you can also create a user `polyaxon` with read only access to your organization repos, and use the username/password. 

## Update your deployment config file and deploy/upgrade

```yaml
reposAccessToken: "username:password"
```

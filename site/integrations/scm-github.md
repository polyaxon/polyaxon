---
title: "Repos on Github"
meta_title: "Github"
meta_description: "How to use code from GitHub repositories on Polyaxon. You can use code from your GitHub repositories directly in Polyaxon projects without having to check them out on your local machine first."
custom_excerpt: "GitHub is an online service for software development projects that use the Git revision control system."
image: "../../content/images/integrations/github.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - scm
featured: true
popularity: 0
visibility: public
status: published
---

You can use code from your GitHub repositories directly in Polyaxon projects without having to check them out on your local machine first.

## Overview

Polyaxon supports repos hosted on GitHub.
You can use code from your GitHub repositories directly in Polyaxon projects without
having to check them out on your local machine first.

N.B. Polyaxon supports public and private GitHub repos, you don't need to have a GitHub account
to use code from public GitHub repositories. e.g. `https://github.com/polyaxon/polyaxon-quick-start`

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

## Create a secret

 * Simple method using an inline token:

```bash
kubectl -n polyaxon create secret generic github-connection-1 --from-literal=POLYAXON_GIT_CREDENTIALS="<TOKEN_HASH>"
```
 * Advanced method using a git credentials store (allows pulling submodules):

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: github-connection-2
type: Opaque
stringData:
  .gitconfig: |
    [credential "https://<HOSTNAME>"]
      helper = store
  .git-credentials: |
    https://<USERNAME>:<TOKEN_HASH>@<HOSTNAME>
```

## Add the repos you want to use to the connections catalog

 * Simple method using the inline token:

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

 * Advanced method using the git cred store:

```yaml
connections:
  - name: repo4
    kind: git
    schema:
      url: https://github.com/org/repo4
    secret:
      name: "github-connection-2"
      mountPath: "/root"
  - name: repo5
    kind: git
    schema:
      url: https://github.com/org/repo5
    secret:
      name: "github-connection-2"
      mountPath: "/root"
```

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

 * Simple method using an inline token:

```bash
kubectl -n polyaxon create secret generic gitlab-connection-1 --from-literal=POLYAXON_GIT_CREDENTIALS="oauth2:<TOKEN_HASH>"
```

 * Advanced method using a git credentials store (allows pulling submodules):

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: gitlab-connection-2
type: Opaque
stringData:
  .gitconfig: |
    [credential "https://<HOSTNAME>"]
      helper = store
  .git-credentials: |
    https://oauth2:<TOKEN_HASH>@<HOSTNAME>
```

## Add the repos you want to use to the connections catalog

 * Simple method using the inline token:

```yaml
connections:
  - name: repo1
    kind: git
    schema:
      url: https://gitlab.com/org/repo1
    secret:
      name: "gitlab-connection-1"
  - name: repo2
    kind: git
    schema:
      url: https://gitlab.com/org/repo2
    secret:
      name: "gitlab-connection-1"
  - name: repo3
    kind: git
    schema:
      url: https://gitlab.com/org/repo3
    secret:
      name: "other-connection"
```

 * Advanced method using the git cred store:

```yaml
connections:
  - name: repo4
    kind: git
    schema:
      url: https://gitlab.com/org/repo4
    secret:
      name: "gitlab-connection-2"
      mountPath: "/root"
  - name: repo5
    kind: git
    schema:
      url: https://gitlab.com/org/repo5
    secret:
      name: "gitlab-connection-2"
      mountPath: "/root"
```

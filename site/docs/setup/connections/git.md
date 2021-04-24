---
title: "Git Connections"
sub_link: "connections/git"
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
sidebar: "setup"
---

Polyaxon allows to use external git providers for code management.

Git connections are how you can authorize your jobs to clone and pull code from different git providers such as Github, Gitlab, and Bitbucket.

## Schema Fields

### url

The url to the git repo to initialize.

```yaml
name: repo-test
kind: git
schema:
  url: https://gitlab.com/org/test
...
```

### Example connection

```yaml
name: repo-test
kind: git
schema:
  url: https://gitlab.com/org/test
secret:
  name: "gitlab-connection"
```


### Example usage as init param

```yaml
params:
  repo:
    connection: "repo-test"
    init: true
```

### Example usage as an init container

Usage with a custom init container

```yaml
run:
  kind: service
  init:
    - connection: "repo-test"
      container: {name: my-own-container, image: ...}
  container:
```


Specific branch or commit:

```yaml
run:
  kind: job
  init:
    - connection: "repo-test"
      git: {revision: branchA}
  container:
```

Overriding the default git url:

```yaml
params:
  kind: job
  init:
    - connection: "repo-test"
      git: {url: https://new.com}
```

Passing flags:

```yaml
params:
  kind: job
  init:
    - connection: "repo-test"
      git: {flags: [--experimental-fetch, --depth 1, --recurse-submodules]}
```

### Example using the connection inside the main container

```yaml
run:
  kind: service
  connections: ["repo-test"]
  container:
```

## Connecting public repos

To add a connection for a public repo, you don't need to set a secret,
for example we can clone `https://github.com/polyaxon/polyaxon-quick-start` github repo:

```yaml
connections:
  ...
  - name: polyaxon-quick-start
    kind: git
    description: Quick start example
    schema:
      url: https://github.com/polyaxon/polyaxon-quick-start
  ...
```

### Run an experiment


You can create a polyaxonfile to run a job that uses a this git repo


```yaml
kind: experiment

build:
  image: tensorflow/tensorflow:1.4.1-py3
  commit: 62b264813aaf5cba3a81919c623ea55c3f79698f
run:
  kind: job
  init:
    - connection: "polyaxon-quick-start"
  container:
    command: [python3, model.py]
```

## Connecting private repos

To use external private repos, you need first to create a secret with an access token or username/password with read access,
to use for your git connection(s).

Read more about some of the [supported platforms](/integrations/scm/).

```yaml
connections:
  ...
  - name: repo1
    kind: git
    description: Repo with data processing code
    schema:
      url: https://github.com/org/private-repo1
    secret:
      name: git-secret
  - name: repo2
    kind: git
    description: Repo with training code
    schema:
      url: https://github.com/org/private-repo2
    secret:
      name: git-secret
  ...
```

### Secret definition

You can create a secret with either:
    * An access token
    * Username and password

The secret must define the environment variable: `POLYAXON_GIT_CREDENTIALS`.

> If you don't need to use the built-in initializer for pulling your code or if you decide to create your own git handler, you can expose any information needed for your logic inside the secret.

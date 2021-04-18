---
title: "SSH Connections"
sub_link: "connections/ssh"
meta_title: "Use SSH to integrate your workflow with external system or to load git repos from github, gitlab, bitbucket in Polyaxon - Configuration"
meta_description: "Polyaxon allows to use ssh connections to connect to external systems and to integrate with git providers for code management."
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

Polyaxon allows to use ssh connections to connect to external systems, including to connect to private or public git repos.

SSH connections can be used as an alternative connection to authorize jobs to clone and pull code from different git providers such as Github, Gitlab, and Bitbucket.

By default, an ssh connection is not automatically used for pulling git repos by Polyaxon unless it is used with a git initializer.

## Schema Fields

### url

It's possible to declare this connection with a schema similar to the git connections, in that case the url will be used as the default git repo to pull.

```yaml
name: repo-test
kind: ssh
schema:
  url: https://gitlab.com/org/test
secret:
  name: "ssh-git-connection"
  mountPath: /etc/.ssh
  defaultMode: 0600
...
```

### Example usage as init param

```yaml
params:
  ssh_param:
    connection: "ssh-git-connection"
```

### Example usage as an init container

Usage with a custom init container

```yaml
run:
  kind: service
  init:
    - connection: "ssh-git-connection"
      container: {name: my-own-container, image: ...}
  container:
```

### Example usage as a git init container

Specific branch or commit:

```yaml
run:
  kind: job
  init:
    - connection: "ssh-git-connection"
      git: {revision: branchA}
  container:
```

Overriding the default git url to pull 2 different repos:

```yaml
params:
  kind: job
  init:
    - connection: "ssh-git-connection"
      git: {url: https://new.com/org/repo1}
    - connection: "ssh-git-connection"
      git: {url: git@another.com:second-org/repo2.git}
```

Passing flags:

```yaml
params:
  kind: job
  init:
    - connection: "ssh-git-connection"
      git: {url: https://new.com/org/repo1}
    - connection: "ssh-git-connection"
      git:
        url: git@another.com:second-org/repo2.git
        flags: [--experimental-fetch, --depth 1, --recurse-submodules]
```

### Example using the connection inside the main container

It's often useful to use an ssh connection to pull an push code changes when running an interactive ide, e.g. VSCode, Notebooks, ...

```yaml
run:
  kind: service
  connections: ["ssh-git-connection"]
  container:
```

## Connecting private repos or generic ssh connection

To use external private repos, you need first to create an ssh secret with access to the repos you want to give access to:

```yaml
connections:
  ...
  - name: repo1
    kind: ssh
    description: SSH connection for Repo1
    schema:
      url: https://github.com/org/private-repo1
    secret:
      name: ssh-secret
      mountPath: /etc/.ssh
      defaultMode: 0600
  - name: repo2
    kind: ssh
    description: SSH connection for Repo2
    schema:
      url: git@github.com:org/private-repo2.git
    secret:
      name: ssh-secret
      mountPath: /etc/.ssh
      defaultMode: 0600
  - name: ssh-connection
    kind: ssh
    description: SSH connection
    secret:
      name: ssh-secret
      mountPath: /etc/.ssh
      defaultMode: 0600
  ...
```

### Secret definition

To create an ssh connection, you need to create a [generic secret with the private and public key](https://kubernetes.io/docs/concepts/configuration/secret/#use-case-pod-with-ssh-keys):

```bash
kubectl create -n polyaxon secret generic ssh-key-secret --from-file=id_rsa=/path/to/.ssh/id_rsa --from-file=id_rsa.pub=/path/to/.ssh/id_rsa.pub
```

In order to mount the ssh connection correctly you need to provide a hidden mount path, e.g. `/etc/.ssh`, and you need to provide how the secret should be mounted `0600`.

If the ssh connection is to be used as an init git container, Polyaxon will look by default for `id_rsa` and `id_rsa.pub` under the mount path, unless the user provides an alternate ssh key name with env var `POLYAXON_SSH_PRIVATE_KEY`.

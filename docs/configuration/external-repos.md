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

In order to set an external repo on a project, the project should not have internal code, i.e. you should not have used `polyaxon upload`.  

## External public repos

To set a public repo on a project you don't need to set any access token, 
for example let's see how we can use the `https://github.com/polyaxon/polyaxon-quick-start` github repo for code tracking:

### Create a project

```bash
polyaxon project create --name=quick-start --description="Quick start using an external repo."
``` 

### Set the git url:

This is where instead of uploading the code, you link to the external repo:

```bash
polyaxon project -p quick-start git --url="https://github.com/polyaxon/polyaxon-quick-start"
```

### Run an experiment


You can create an polyaxonfile to run:

```yaml
kind: expiriment

build:
  image: tensorflow/tensorflow:1.4.1-py3

run:
  cmd: python3 model.py
```

and then run:

```bash
polyaxon project -p quick-start -f polyaxonfile.yaml
```

This will start an experiment the specification we just create with the latest git commit of the repo on github.

You can also, specify which commit or branch to run, update the polyaxonfile with a specific [commit](https://github.com/polyaxon/polyaxon-quick-start/commit/62b264813aaf5cba3a81919c623ea55c3f79698f):


```yaml
kind: expiriment

build:
  image: tensorflow/tensorflow:1.4.1-py3
  commit: 62b264813aaf5cba3a81919c623ea55c3f79698f

run:
  cmd: python3 model.py
```

and then run it:

```bash
polyaxon project -p quick-start -f polyaxonfile.yaml
```

Same thing is possible with notebook, labs, tensorboards, and jobs.

## External private repos

To use external private repos, you need first to deploy/upgrade your deployment with a access token or username/password with read access, 
read more about some of the [supported platforms](/integrations/scm/).


### Deploying with an access token

```yaml
reposAccessToken: "TokenHashHere"
```

### Deploying with username and password

```yaml
reposAccessToken: "username:password"
```

### Create a project

```bash
polyaxon project create --name=private-repo --description="My private external repo."
``` 

### Set the git url

```bash
polyaxon project -p private-repo git --url="https://platform.com/org/private-repo" --private
```

> it's important to add `--private`, this tells Polyaxon to use the access token, username/password when interacting with external platform.

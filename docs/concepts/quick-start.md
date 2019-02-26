---
title: "Quick Start"
sub_link: "quick-start"
meta_title: "Polyaxon quick start tutorial - Core Concepts"
meta_description: "Get started with Polyaxon and become familiar with the ecosystem of Polyaxon with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - quick-start
sidebar: "concepts"
---

Let’s look at an example of how you can use Polyaxon for your deep learning experiments.
This example assumes that both Polyaxon is [installed](/setup/) and running.
And you are logged in to your Polyaxon account through the [polyaxon-cli](/references/polyaxon-cli/auth/)


### Check that your cli is configured and you are logged in

The first step is to check that you are logged in and that you are running a version of CLI compatible with the platform.

```bash
polyaxon version --cli
```

```bash
polyaxon version --platform
```

```bash
polyaxon whoami
```

### Check the cluster discovery

Check that polyaxon is reporting your cluster correctly

```bash
$ polyaxon cluster

Cluster info:

--------------  ----------------------------------------
build_date      2017-11-20T05:17:43Z
major           1
go_version      go1.8.3
git_version     v1.8.4
platform        linux/amd64
git_commit      9befc2b8928a9426501d3bf62f72849d5cbcd5a3
git_tree_state  clean
minor           8
compiler        gc
--------------  ----------------------------------------

Cluster Nodes:

  id  name                       hostname                   role    memory      n_cpus    n_gpus
----  -------------------------  -------------------------  ------  --------  --------  --------
   1  k8s-agentpool1-13475325-0  k8s-agentpool1-13475325-0  agent   6.7 Gb           2         0
   2  k8s-agentpool2-13475325-0  k8s-agentpool2-13475325-0  agent   54.93 Gb         6         1
   3  k8s-master-13475325-0      k8s-master-13475325-0      master  6.7 Gb           2         0
```

### Create a project 

Now we can create a project, you can do that with `Polyaxon Dashboard` or with `polyaxon CLI`

```bash
$ polyaxon project create --name=quick-start --description='Polyaxon quick start.'
```

### Prepare your code 

Polyaxon offers 2 options for tracking code, an in-cluster git server or tracking code on external platforms (Github, GitLab, Bitbucket, ...).

A project can only be linked to one repo (either in-cluster or on Github for example), in both cases, your workflow will be mor or less similar. 

We have created 2 quick-start guides to show how you can use each one of this options:

  * A [guide](/concepts/quick-start-internal-repo/) to track code in-cluster.
  * A [guide](/concepts/quick-start-external-repo/) to track code on Github (N.B. you can use any other platform by just changing the repo url). 

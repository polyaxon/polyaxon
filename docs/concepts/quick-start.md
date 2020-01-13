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

### Create a project 

Now we can create a project, you can do that with `Polyaxon Dashboard` or with `polyaxon CLI`

```bash
$ polyaxon project create --name=quick-start --description='Polyaxon quick start.'
```

### Prepare your code 

Polyaxon offers 2 options for tracking code, an in-cluster git server or tracking code on external platforms (Github, GitLab, Bitbucket, ...).

A project can only be linked to one repo (either in-cluster or on Github for example), in both cases, your workflow will be more or less similar. 

We have created 2 quick-start guides to show how you can use each one of this options:

  * A [guide](/concepts/quick-start-internal-repo/) to track code in-cluster.
  * A [guide](/concepts/quick-start-external-repo/) to track code on Github (N.B. you can use any other platform by just changing the repo url). 

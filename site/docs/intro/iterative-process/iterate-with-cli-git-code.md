---
title: "Iterate with Polyaxon CLI and a remote git repo"
sub_link: "iterative-process/iterate-in-notebooks"
meta_title: "Iterate with Polyaxon CLI - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Iterate with Polyaxon CLI - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - notebook
  - quick-start
sidebar: "intro"
---

We previously learned how to run operations with Polyaxonfiles hosted on Github using the `--url` argument.
But during a rapid development, users will want to iterate on their code and submit operations with those changes.

In this sections we will learn how to initialize a local folder and integrate it with a repo using a git connection or using a public repo.

> **Note**: To integrate your local code with the CLI, please check the previous section of this guide.

## Clone Polyaxon quick-start

Head to your terminal and clone the [quick-start](https://github.com/polyaxon/polyaxon-quick-start) repo


```bash
git clone https://github.com/polyaxon/polyaxon-quick-start.git
```

And change to the subpath `git-integration`

```bash
cd polyaxon-quick-start/git-integration
```

We only have one simple polyaxonfile which we will use for this example, it's the same as the `simple.yaml` file that we used before under `experimentation`,
the only difference is that this version does not include an init section.

```yaml
version: 1.1
kind: component
name: simple-experiment
description: Minimum information to run this TF.Keras example
tags: [examples, local-git]
run:
  kind: job
  container:
    image: polyaxon/polyaxon-quick-start
    workingDir: "{{ globals.artifacts_path }}/polyaxon-quick-start"
    command: [python3, model.py]
```   

## Initialize the project

Instead of hard-coding an init section like in the previous sections of this quick-start tutorial, 
we will initialize this local path with a git integration that we can use to integrate automatically with our polyaxonfiles.

The [init](/docs/core/cli/init/) command accepts both a `--git-connection` and `--git-url`. If you are using a private git repo, 
you will need to configure a [git connection](/docs/setup/connections/git/) and redeploy Polyaxon first.

> To initialize the folder with a private repo you need a valid `--git-connection`, you can additionally override the default git repo of that connection by providing the `--git-url` argument. 

In the context of this tutorial, we are using a public github repo that does not require a git connection, so we will initialize this folder with a `git-url` only.

```yaml
polyaxon init -p quick-start --git-url https://github.com/polyaxon/polyaxon-quick-start
```

## Scheduling experiments after every commit

In the previous section of this tutorial we were using a hard-coded git initializer, the git initializer did not have any fixed revision, 
which means that every time we submit a job, Polyaxon will pull the latest commit from the remote repo, the commit could be made by us or by another user. 
By initializing a local folder we can now run operations based on changes made by us, because the CLI will patch the polyaxonfile with a code version before submitting new operations:

```bash
git commit -am "Update" 
git push orgin master
polyaxon run -f simple.yaml --git-preset
```

The last command will tell Polyaxon to look for the git configuration that we initialized earlier in this folder and detect the latest commit and inject it as a [preset](/docs/core/scheduling-presets/).

## Scheduling experiments with specific commits or branches

We can also schedule experiments with a specific git commit, a specific branch, or a valid tree-ish:

```bash
polyaxon run -f simple.yaml --git-preset --git-revision="dev"
```

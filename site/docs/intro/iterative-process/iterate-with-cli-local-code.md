---
title: "Iterate with Polyaxon CLI and a local project"
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

> **Note**: Requires Polyaxon v1.3.3 or higher.

We previously learned how to run operations with Polyaxonfiles hosted on Github using the `--url` argument.
But during a rapid development, users will want to iterate on their code and submit operations with those changes.

In this sections we will learn how to initialize a local folder and run ab interactive experimentation process by uploading the code to the experiment's path on the artifacts store.

> **Note**: To integrate an external git repo with the CLI, please check the next section of this guide. 

## Clone Polyaxon quick-start

Head to your terminal and clone the [quick-start](https://github.com/polyaxon/polyaxon-quick-start) repo

```bash
git clone https://github.com/polyaxon/polyaxon-quick-start.git
```

## Check the polyaxonfile for the local integration

Under the path `local-integration` there's a single polyaxonfile which we will use for this example, it's the same as the `simple.yaml` file that we used before under `experimentation`,
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
    workingDir: "{{ globals.run_artifacts_path }}/uploads"
    command: [python3, model.py]
```

Another thing to notice about this polyaxonfile is that we have a different `workingDir: "{{ globals.run_artifacts_path }}/uploads"`.
We are telling our container to use the `uploads` under the run artifacts path.

the value `/uploads` can be any subpath you decide to upload your local code to, the default one is `uploads`.

## Initialize the project

Instead of hard-coding an init section like in the previous sections of this quick-start tutorial, 
we will initialize this local path to be able to leverage the CLI cache and avoid passing the project to all commands:

```yaml
polyaxon init -p quick-start --polyaxonignore
```

You will be prompted to override the current `polyaxonignore`, just say no because this example already has one, 
but in other project in order to avoid uploading all files you should have a `.polyaxonignore`. 
For instance to make the upload optimized and fast you should not upload your `.git` history, the IDE config, ... 

## Uploading and scheduling experiments

In the previous section of this tutorial we were using a hard-coded git initializer, which requires a git push and a connection to handle the pull if the repo is private.
 
In this section we will upload the local code instead before starting an operation:

```bash
polyaxon run -f local-integration/simple.yaml -u
```

This will tell Polyaxon to upload anything from the current path, while respecting the `.polyaxonignore` pattern, before starting the experiment.

## Uploading and scheduling experiments using a different path

If you want to upload the code, or any artifacts, to a different path other than the default `uploads`, 
for instance to use `code` you should do the following:

 * Change the `workingDir: "{{ globals.run_artifacts_path }}/code"` in the polyaxonfile
 * Run the upload command with a specific path: `polyaxon run -f local-integration/simple.yaml -u-to code`
 
If your local folder is large, and several subpaths are not necessary, you can also use `-u-from/--upload-from`.

> **Note**: It's possible to remove the `workingDir` altogether and put that logic in presets.
> This will allow you to use the same polyaxonfiles and patch them based on if you are using a git repo or local code. 

## Uploading after starting an experiment

Polyaxon CLI provides a command: `polyaxon ops upload --help` which has more options that allows to upload artifacts to an already created experiment independently of its current status.

This command is helpful if you need to upload some artifacts or some code, or resume a previous operation with different artifacts.

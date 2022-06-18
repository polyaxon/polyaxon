---
title: "Iterate with Presets"
sub_link: "iterative-process/iterate-with-presets"
meta_title: "Iterate with Presets - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Using presets to improve the process of using git and code upload - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
  - tutorials
  - concepts
  - client
  - quick-start
sidebar: "intro"
---

> **Note**: This is an advanced use-case that you might want to skip for now and come back to later. 

We previously learned how to configure the CLI to iterate with:
 * [local code](/docs/intro/iterative-process/iterate-with-cli-local-code/)
 * [git repo](/docs/intro/iterative-process/iterate-with-cli-git-code/)

In both guides, we had to adjust the polyaxonfile to fit a specific workflow.
Often, users will probably need to use both workflows to iterate on their experiments, for quick changes they will need to upload code directly before starting a run, 
and after committing the changes they will need to trigger based on the git repo, 
finally, they might need to have the manifest compatible with a fork of their main repo or a repo that is named differently.    

In this guide, we will learn how to improve our polyaxonfile to adapt it to different situations with presets.

## Remove the git initializer from the component

In order to make the component work in different situations, i.e. get executed based on an initialized git repo or from local code, we will start by removing the git initializer and the `container.workingDir` section:

```yaml
version: 1.1
kind: component
name: typed-experiment
description: experiment with inputs
tags: [examples]

inputs:
- {name: conv1_size, type: int, value: 32, isOptional: true}
- {name: conv2_size, type: int, value: 64, isOptional: true}
- {name: dropout, type: float, value: 0.2, isOptional: true}
- {name: hidden1_size, type: int, value: 500, isOptional: true}
- {name: conv_activation, type: str, value: relu, isOptional: true}
- {name: dense_activation, type: str, value: relu, isOptional: true}
- {name: optimizer, type: str, value: adam, isOptional: true}
- {name: learning_rate, type: float, value: 0.01, isOptional: true}
- {name: epochs, type: int}
outputs:
- {name: loss, type: float}
- {name: accuracy, type: float}

run:
  kind: job
  container:
    image: polyaxon/polyaxon-quick-start
    command: ["python3", "model.py"]
    args: [
      "--conv1_size={{ conv1_size }}",
      "--conv2_size={{ conv2_size }}",
      "--dropout={{ dropout }}",
      "--hidden1_size={{ hidden1_size }}",
      "--optimizer={{ optimizer }}",
      "--conv_activation={{ conv_activation }}",
      "--dense_activation={{ dense_activation }}",
      "--learning_rate={{ learning_rate }}",
      "--epochs={{ epochs }}"
    ]
```

You can view this file under `presets/`, we also have other files under that folder that we will use with this component.

If we try to execute this component, it will fail, since the container cannot resolve the file `model.py`.

We can additionally make this manifest fail fast at the CLI level, in other terms, 
we can prevent users from attempting to submit this file, wait for the operation to be scheduled, 
and then check the logs to find out that the container is missing the code. 
Polyaxon's specification has a section called `template` that we can add to any polyaxonfile to prevent running it without proper initialization:

```yaml
template:
  enabled: true
  description: "This polyaxonfile requires a preset to run correctly."
  fields: ["runPatch.container.workingDir"]
```

> **Note**: You can learn more about the [template section here](/docs/core/specification/template/) 

## Using the local code preset

In this subsection we will run `presets/polyaxonfile.yaml` with `presets/upload-workingdir-preset.yaml`:

```bash
polyaxon run -f presets/polyaxonfile.yaml -f presets/upload-workingdir-preset.yaml -u -l
```

By running this command we will supplement the main component with the additional section that resolves the path to `model.py` from the uploaded code:

```yaml
runPatch:
  container:
    workingDir: "{{ globals.run_artifacts_path }}/uploads"
```

## Using the git integration

In this subsection we will run `presets/polyaxonfile.yaml` with `presets/git-workingdir-preset.yaml` and the `--git-preset` flag:

In this case we will use both the [git-preset integration](/docs/intro/iterative-process/iterate-with-cli-git-code/) 
if set, and supplement the main component with the additional section that resolves the path to `model.py` from the initialized code:

```bash
polyaxon run -f presets/polyaxonfile.yaml -f presets/git-workingdir-preset.yaml --git-preset -l
```

By running this command we will supplement the main component with the additional section that resolves the path to `model.py` from the git integration:

```yaml
runPatch:
  container:
    workingDir: "{{ globals.artifacts_path }}/polyaxon-quick-start"
```

## Using the custom git preset and git workingDir

In this subsection we will run `presets/polyaxonfile.yaml` with `presets/git-init.yaml` and `presets/git-workingdir-preset.yaml`:

This is similar to the previous subsection, the only difference is that we do not use `--git-preset` but instead we provide our own `presets/git-init.yaml` file:

```bash
polyaxon run -f presets/polyaxonfile.yaml -f presets/git-workingdir-preset.yaml -f presets/git-init.yaml -l
```

By running this command we will supplement the main component with the additional section that resolves the path to `model.py` from the git preset:

```yaml
runPatch:
  container:
    workingDir: "{{ globals.artifacts_path }}/polyaxon-quick-start"
```

## More presets

In this guide we only extracted the logic for initializing/uploading the code and for setting the `workingDir`, but presets are a very powerful feature in Polyaxon, 
it allows users to define several reusable configurations, e.g. complex node selectors, resources requirements, ...

You can check the folder [helpers](https://github.com/polyaxon/polyaxon-quick-start/tree/master/helpers) which contains additional preset examples. 

> For mode details about using presets please check the [scheduling presets guide](/docs/core/scheduling-presets/) 

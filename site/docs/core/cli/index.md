---
title: "Polyaxon CLI"
sub_link: "polyaxon-cli"
meta_title: "Polyaxon Command Line Interface Specification - Polyaxon References"
meta_description: "Polyaxon Command Line Interface Specification."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
sidebar: "core"
---

Polyaxon CLI is a tool and a client to interact with Polyaxon,
it allows you to manage your cluster, projects, and experiments.

## Installation

To install Polyaxon CLI please refer to the [installation documentation](/setup/cli/).


## Help

To get help from The Polyaxon CLI, you can run the following

```bash
$ polyaxon --help
```

To get help for any Polyaxon CLI Command, you can run the following

```bash
$ polyaxon command --help
```

## Commands References

 * [Auth](auth/)
 * [Admin](admin/)
 * [Completion](completion/)
 * [Check](check/)
 * [Config](config/)
 * [Init](init/)
 * [Project](project/)
 * [Upload](Upload/)
 * [Run](run/)
 * [Ops](ops/)
 * [Dashboard](dashboard/)
 * [Version](version/)

## Caching

When using the Polyaxon CLI to run a command requiring a project or a run,
you can always specify the values for these options, example:

 * `$ polyaxon project --project=user_1/project_10 get`
 * `$ polyaxon ops --project=user_1/project_10 --uid=UUID get`


Polyaxon CLI allows also you to omit these options, i.e. project, experiment group, experiment, and job, the CLI does the following:

 1. When a username is missing, the username of the logged-in user is used.
 2. When a project name is missing, the name of the currently initialized project is used.
 3. When an experiment group, experiment, or job is missing, the last value is used.
 4. If no values are found, the CLI will show an error.

All commands and sub-command of `project` and `ops` support caching:

 * `$ polyaxon project ls`
 * `$ polyaxon project get`
 * `$ polyaxon ops ls`
 * `$ polyaxon ops get`
 * `$ polyaxon ops logs`
 * ...

## Switching context

Users don't have to change to a new project to access information about that project, and its ops.

All commands allow to change the project context by providing `-p project` or `--project=project`.

You can as well check other users/organizations projects without initializing the projects, `-p owner/project` or `--project=owner/project`.

Here are some examples:

 * Getting other projects experiments:
 
    * `polyaxon project -p mnist ops -s "-created_at"`
    * `polyaxon project --project=adam/mnist ops -q "status: failed"`
    
 * Getting services named `tensorboard` for some projects:
 
    * `polyaxon ops --project=mnist ls --query="name: tensorboard" --sort="-created_at"`
    * `polyaxon tensorboards -p adam/mnist ls --query="name: tensorboard, status: running"`

 * Getting information about a specific experiment:
 
    * `polyaxon ops -p mnist -uid UUID get`
    * `polyaxon ops -p adam/mnist --uid=UUID get`

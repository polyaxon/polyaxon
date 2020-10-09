---
title: "Polyaxon CLI"
sub_link: "polyaxon-cli"
meta_title: "Polyaxon Command Line Interface Specification - Polyaxon References"
meta_description: "Polyaxon Command Line Interface Specification."
visibility: public
status: published
is_index: true
tags:
    - cli
    - reference
    - polyaxon
sidebar: "core"
---

Polyaxon CLI is a tool and a client to interact with Polyaxon,
it allows you to manage your cluster, projects, and experiments.

## Installation

To install Polyaxon CLI please refer to the [installation documentation](/docs/setup/cli/).

## Help

To list all commands and get information about Polyaxon CLI, you can run the following

```bash
$ polyaxon --help
```

To get help for any Polyaxon CLI Command, you can run the following

```bash
$ polyaxon command --help
```

Some commands have sub-commands, you can also get help for these sub-commands by running

```bash
$ polyaxon command sub-command --help
```

## Deprecated behavior

Polyaxon used to pass a context between commands and subcommands, e.g.

```bash
polyaxon ops -p PROJECT -uid UID get --more-args
```

This behavior was confusing and the help command did not show the complete information about running a specific command.
We deprecated this behavior in favor of putting all arguments in front of the last sub-command, e.g.

```bash
polyaxon ops get -p PROJECT -uid UID --more-args
```

## Caching

When using Polyaxon CLI to run a command requiring a project or a run,
you can always specify the values for these options, for example:

 * `$ polyaxon project get --project=user_1/project_10`
 * `$ polyaxon ops get --project=user_1/project_10 --uid=UUID`


Polyaxon CLI allows also you to omit these options for projects and runs, the CLI does the following:

 1. When an owner (username or an organization) is missing, the owner is inferred based on the logged-in user, if no user/owner is found the default owner is used.
 2. When a project name is missing, the name of the currently initialized project is used.
 3. When a run is missing, the last value is used.
 4. If no values are found, the CLI will show an error.

All commands and sub-command of `project` and `ops` support this caching mechanism:

 * `$ polyaxon project ls`
 * `$ polyaxon project get`
 * `$ polyaxon ops ls`
 * `$ polyaxon ops get`
 * `$ polyaxon ops logs`
 * ...

## Updating the cached configuration

Every time you create a project or start a run, Polyaxon will save the response of that entity to the cache. For example:

`polyaxon project create --name test` will create a new project and will automatically cache the value of that project.
In all subsequent commands, if the user does not provide a project `--project`, Polyaxon CLI will use this project that was created.

`polyaxon run ...` will create a new run and will automatically cache the value.
In all subsequent commands, if the user does not provide a project `--project/-p` and a run uuid `--uid/-uid`, Polyaxon CLI will use the last cached project and run.

By creating new runs, Polyaxon will keep updating the cache detail to the latest created run.

You can also influence the run cache by getting a specific run, e.g. `polyaxon ops get -uid UUID` 
will fetch the information about that specific run and persist the result to the cache so that you can run further commands 
without the need to pass the `-uid UUID`, e.g. `polyaxon ops logs` will use the same `UUID`.

## Caching visibility

By default, Polyaxon will cache all information on Polyaxon's global path, if you want to enable caching on local project folder(s), you can use the init command:

```bash
$ polyaxon init -p PROJECT_NAME
```

This will create a local cache folder for the project and its runs.

Anytime you use the cli, it will look first locally, then defaults to the global path.

## Switching context

Users don't have to change to a new project to access information about that project, and its ops.

All commands allow to change the project context by providing `-p project` or `--project=project`.

You can as well check other users/organizations projects without initializing the projects, `-p owner/project` or `--project=owner/project`.

Here are some examples:

 * Getting other projects experiments:

    * `polyaxon project ops -p mnist -s "-created_at"`
    * `polyaxon project ops --project=adam/mnist -q "status: failed"`

 * Getting services named `tensorboard` for some projects:

    * `polyaxon ops ls --project=mnist --query="name: tensorboard" --sort="-created_at"`
    * `polyaxon tensorboards ls -p adam/mnist --query="name: tensorboard, status: running"`

 * Getting information about a specific experiment:

    * `polyaxon ops get -p mnist -uid UUID`
    * `polyaxon ops get -p adam/mnist --uid=UUID`

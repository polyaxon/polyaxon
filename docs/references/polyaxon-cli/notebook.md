---
title: "Notebook"
sub_link: "polyaxon-cli/notebook"
meta_title: "Polyaxonfile Command Line Interface Specification - Notebook - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Notebook."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - notebook
sidebar: "polyaxon-cli"
---

> Some commands in this sections require a Polyaxon deployment with scheduler enabled

> You can always access the help menu for this command by adding `--help`

The project commands accept an optional argument `--project` or '-p'  to use a specific project.

If no project is provided, the command will default to the currently initialized project.

If no project is provided and no project is cached, the command will raise an error.


Usage:

polyaxon notebook [OPTIONS] COMMAND [ARGS]...

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT |
  --help | | Show this message and exit.


## start

Usage:

```bash
$ polyaxon notebook start
```

Start a notebook deployment for this project.


Uses [Caching](/references/polyaxon-cli/#caching)


Example:

Example specifying the polyaxonfile

```bash
$ polyaxon notebook start -f file -f file_override ...
```

Example upload before running

```bash
$ polyaxon -p user12/mnist notebook start -f file -u
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  -u | | To upload the repo before running.
  --help | | Show this message and exit.

## stop

Usage:

```
$ polyaxon notebook stop
```

Stops the notebook deployment for this project if it exists.

Uses [Caching](/references/polyaxon-cli/#caching)


option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## url

Prints the notebook url for this project.

Uses [Caching](/references/polyaxon-cli/#caching)

Example:

```bash
$ polyaxon notebook url
```

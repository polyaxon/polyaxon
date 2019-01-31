---
title: "Run"
sub_link: "polyaxon-cli/run"
meta_title: "Polyaxonfile Command Line Interface Specification - Run - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Run."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - run
sidebar: "polyaxon-cli"
---

> This command can only be used for a Polyaxon deployment with a scheduler enabled

> You can always access the help menu for this command by adding `--help`

Usage:

```bash
$ polyaxon run [OPTIONS]
```

Run polyaxonfile specification.

Examples:

```bash
$ polyaxon run -f file -f file_override ...
```

Upload before running

```bash
$ polyaxon run -f file -u
```

Start logs after running

```bash
$ polyaxon run -f file -u -l
```

Run and add a ttl of 60 seconds after the experiment is done (succeeds or fails)

```bash
$ polyaxon run -f file --ttl=60
```

Run and set description and tags for this run

```bash
$ polyaxon run -f file -u --description="Description of the current run" --tags="foo, bar, moo"
```
Run and set a unique name for this run

```bash
polyaxon run --name=foo
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  --name [optional] | TEXT | Name to give to this run, must be unique within the project, could be none.
  --description [optional] | TEXT | The description to give to this run.
  --tags [optional] | TEXT | Tags of this run, comma separated values.
  --ttl [optional] | INT | Time to live for the current run after it's done.
  -l [optional] | | To start logs after running.
  -u [optional] | | To upload the repo before running.
  --help | | Show this message and exit.

---
title: "Config"
sub_link: "polyaxon-cli/config"
meta_title: "Polyaxonfile Command Line Interface Specification - Config - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Config."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - config
sidebar: "polyaxon-cli"
---

> This command can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

Set and get global configurations.

## Get global config by keys

Usage:

```bash
$ polyaxon config get [OPTIONS] [KEYS]...
```

Get the global config values by keys.

Example:

```bash
$ polyaxon config get host port
```

## Set global config keys

Usage:

```bash
$ polyaxon config set [OPTIONS]
```

Set the global config values.

Example:

```bash
$ polyaxon config set --host=localhost --port=80
```

Options:

option | type | description
-------|------|------------
  --verbose| BOOLEAN | To set the verbosity of the client.
  --host| TEXT | To set the server endpoint.
  --port| INTEGER | To set the http port.
  --use_https| BOOLEAN | To set the https.
  --help| | Show this message and exit..

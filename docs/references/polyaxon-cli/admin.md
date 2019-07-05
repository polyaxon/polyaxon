---
title: "Admin"
sub_link: "polyaxon-cli/admin"
meta_title: "Polyaxonfile Command Line Interface Specification - Admin - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Admin."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - admin
sidebar: "polyaxon-cli"
---

> You can always access the help menu for this command by adding `--help`

## admin

Usage:

```bash
$ Usage: polyaxon admin [OPTIONS] COMMAND [ARGS]...
```

Commands for admin management.


## deploy    

Usage: 

```bash
polyaxon admin deploy [OPTIONS]
```

Deploy polyaxon.

Options:

option | type | description
-------|------|------------
  -f, --file | PATH |      The polyaxon deployment config file(s) to check.
  --manager_path | PATH | The path of the deployment manager, e.g. local chart.
  --check |  | Check if deployment file and other requirements are met.
  --dry_run |  | Dry run the configuration and generate a debuggable output.
  --help |  | Show this message and exit.

## upgrade   

Usage: 

```bash
polyaxon admin upgrade [OPTIONS]
```

Upgrade a Polyaxon deployment.

Options:

option | type | description
-------|------|------------
  -f, --file | PATH |      The polyaxon deployment config file(s) to check.
  --manager_path | PATH | The path of the deployment manager, e.g. local chart.
  --check |  | Check if deployment file and other requirements are met.
  --dry_run |  | Dry run the configuration and generate a debuggable output.
  --help |  | Show this message and exit.

## teardown  


```bash
polyaxon admin teardown [OPTIONS]
```

Teardown a polyaxon deployment given a config file.

Options:

option | type | description
-------|------|------------
  -f, --file | PATH |      The polyaxon deployment config file(s) to check.
  --help |  | Show this message and exit.

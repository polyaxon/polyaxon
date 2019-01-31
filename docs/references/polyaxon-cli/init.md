---
title: "Init"
sub_link: "polyaxon-cli/init"
meta_title: "Polyaxonfile Command Line Interface Specification - Init - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Init."
visibility: public
status: published
tags:
    - cli
    - polyaxon
    - reference
    - init
sidebar: "polyaxon-cli"
---

> This command can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

Usage:

```bash
$ polyaxon init [OPTIONS] PROJECT
```

Initialize a new polyaxonfile specification.

Options:

option | description | default
-------|-------------|---------
  --run | Init a polyaxon file with `exec` step template. | True
  --model | Init a polyaxon file with `model` step template. |
  --help | Show this message and exit. |

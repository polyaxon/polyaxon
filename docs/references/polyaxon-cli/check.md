---
title: "Check"
sub_link: "polyaxon-cli/check"
meta_title: "Polyaxonfile Command Line Interface Specification - Check - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Check."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - check
sidebar: "polyaxon-cli"
---

> This command can only be used for a Polyaxon deployment with a scheduler enabled

> You can always access the help menu for this command by adding `--help`

Check the validity of a polyaxonfile.yml.

Usage:
```bash
$ polyaxon check [OPTIONS]
```

Check a polyaxonfile.

Options:

option| type | description
------|------|------------
  -f, --file| PATH| The polyaxon file to check.
  -v, --version| | Checks and prints the version.
  -def, --definition| | Checks and prints the file definition.
  --help| | Show this message and exit.

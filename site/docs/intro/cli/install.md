---
title: "How to install Polyaxon CLI"
sub_link: "cli/install"
meta_title: "A guide on how to install Polyaxon CLI - Core Concepts"
meta_description: "Polyaxon CLI is a Python command-line interface to interact with Polyaxon API."
visibility: public
status: published
tags:
  - concepts
  - tutorials
sidebar: "intro"
---

Polyaxon CLI is a Python command-line interface to interact with Polyaxon API.


## Install

To install it simply run:

```bash
pip install -U polyaxon
```

N.B. `polyaxon` library is a Python 3.5+ package, if you are still using Python 2 `polyaxon-sdk` is Python 2/3 compatible.

## Help

To list all commands and get information about Polyaxon CLI, you can run the following

```bash
polyaxon --help
```

To get help for any Polyaxon CLI Command, you can run the following

```bash
polyaxon command --help
```

Some commands have sub-commands, you can also get help for these sub-commands by running

```bash
polyaxon command sub-command --help
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

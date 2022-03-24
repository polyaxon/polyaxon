---
title: "Polyaxon CLI"
sub_link: "cli"
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

## Overview

Polyaxon CLI is a tool and a client to interact with Polyaxon API, it allows you to manage your cluster, projects, and experiments.
This section has several common guides on how to configure and use the CLI followed by several reference pages for each command.

## Install

To install it simply run:

```bash
pip install -U polyaxon
```

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

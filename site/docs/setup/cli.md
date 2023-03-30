---
title: "Install Polyaxon CLI"
title_link: "Install Polyaxon CLI"
sub_link: "cli"
date: "2018-10-01"
meta_title: "How to install Polyaxon CLI"
meta_description: "Polyaxon CLI is a Python command line interface to interact with Polyaxon API."
tags:
  - cli
  - install
sidebar: "setup"
---

Polyaxon CLI is a Python command line interface to interact with Polyaxon API.


## Install

To install it simply run:

```bash
pip install -U polyaxon
```

## Configure

In order for Polyaxon CLI to work correctly,
you must execute the steps in the `NOTES` from [Polyaxon Helm deployments](/docs/setup/).

Those steps ensures that, you configure Polyaxon to connect to the correct host on the correct ports.


After installing the CLI you can view the commands supported using the `--help` option.

```bash
polyaxon --help
```

For more information please have a look [Polyaxon CLI section](/docs/core/cli/).


## Login

If you are using **Polyaxon Cloud or Polyaxon EE**, you can authenticate your CLI by running the following command

```bash
polyaxon login --username=<USERNAME>
```

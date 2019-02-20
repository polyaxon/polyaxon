---
title: "Install on Polyaxon CLI"
title_link: "Install on Polyaxon CLI"
sub_link: "cli"
date: "2018-10-01"
meta_title: "How to install Polyaxon CLI"
meta_description: "Polyaxon CLI is a python command line interface to interact with Polyaxon API."
tags:
    - cli
    - install
---

Polyaxon CLI is a python command line interface to interact with Polyaxon API.


## Install

To install it simply run:

```bash
pip install -U polyaxon-cli
```

and to install the CLI for python3 usage

```bash
pip3 install -U polyaxon-cli
```


## Configure

In order for polyaxon CLI to work correctly,
you must execute the steps in the `NOTES` from [polyaxon helm deployments](/setup/kubernetes/).

Those steps ensures that, you configure Polyaxon to connect to the correct host on the correct ports.


After installing the CLI you can view the commands supported using the `--help` option.

```bash
$ polyaxon --help
```

For more information please have a look [polyaxon cli section](/references/polyaxon-cli/).


## Login

To authenticate your CLI, run the following command

```bash
$ polyaxon login --username=<USERNAME>
```

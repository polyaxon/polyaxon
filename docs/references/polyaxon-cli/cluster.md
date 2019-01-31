---
title: "Cluster"
sub_link: "polyaxon-cli/cluster"
meta_title: "Polyaxonfile Command Line Interface Specification - Cluster - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Cluster."
visibility: public
status: published
tags:
    - cli
    - polyaxon
    - reference
    - cluster
    - management
sidebar: "polyaxon-cli"
---

> Some commands in this sections can only function correctly when Polyaxon is deployed on Kubernetes

> You can always access the help menu for this command by adding `--help`

Usage:
```bash
$ polyaxon cluster [OPTIONS]
```

Get cluster and nodes info.

Options:

option | type | description
-------|------|------------
  --node| TEXT|
  --help| | Show this message and exit.

Example

Get cluster info

```bash
$ polyaxon cluster
```

Get node info

```bash
$ polyaxon cluster -n 2
```

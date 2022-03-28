---
title: "How to reconfigure Polyaxon CLI"
sub_link: "cli/reconfiguration"
meta_title: "A guide on how to reconfigure Polyaxon CLI - Core Concepts"
meta_description: "Polyaxon CLI can connect to many deployments."
visibility: public
status: published
tags:
  - cli
  - reference
  - polyaxon
  - concepts
  - tutorials
sidebar: "core"
---

## Overview

Polyaxon CLI can be configured using several options and can connect to multiple Polyaxon deployments.

The below command shows the help for all sub-commands and options:

```bash
polyaxon config --help
```

> For more details about this command please check the [command reference](/docs/core/cli/config/)

## Connecting to different hosts

In order to connect Polyaxon CLI to a different host: 

```bash
polyaxon config set --host=IP [--no-purge]
```

or 

```bash
polyaxon config set --host=https://IP:PORT [--no-purge]
```

or 

```bash
polyaxon config set --host=http://localhost:PORT [--no-purge]
```


or 

```bash
polyaxon config set --host=https://polyaxon.acme.com [--no-purge]
```

When a user reconfigures their CLI, it will automatically purge all previous configurations and will reset the auth information, in order to avoid resetting the previous configuration and only change the host:

```bash
polyaxon config set --host=https://polyaxon.acme.com --no-purge
```

## Configuration using environment variable

You can configure your CLI directly via environment variables, this tends to be useful when using the CLI in a CI/CD system.

Polyaxon provides several options, the main ones are:

```bash
export POLYAXON_HOST ...
export POLYAXON_VERIFY_SSL ...
export POLYAXON_SSL_CA_CERT ...
export POLYAXON_CERT_FILE ...
export POLYAXON_KEY_FILE ...
export POLYAXON_DEBUG ...
export POLYAXON_TIMEOUT ...
export POLYAXON_LOG_LEVEL ...
```

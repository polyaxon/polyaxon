---
title: "Customize git preset"
sub_link: "cli/customize-git-preset"
meta_title: "A guide on how to customize the remote git preset integration - Core Concepts"
meta_description: "Polyaxon allows to iterate with Polyaxon CLI and a remote git repo, this guide shows how users can extend or create their own polyaxongit.yaml file."
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

Polyaxon CLI allows to initialize a local folder and provides an integration with a repo using a git connection or using a public repo. 
This guide shows how users can extend or create their own `polyaxongit.yaml` file.


### CLi init command

To initialize a local folder with a remote repo using Polyaxon CLI:

```yaml
polyaxon init -p PROJECT_NAME --connection CONNECTION_NAME
```

Or for a public repo

```yaml
polyaxon init -p PROJECT_NAME --git-url https://github.com/org/repo-name
```

Or to use a connection and a custom repo url

```yaml
polyaxon init -p PROJECT_NAME --connection CONNECTION_NAME --git-url https://github.com/org/repo-name
```

> **Note**: For more information, please run `polyaxon init --help`

When executing one of the above commands, Polyaxon will create a file `polyaxongit.yaml` that contains a [preset](/docs/core/scheduling-presets/).

### Using the git-preset argument

In order to trigger the `polyaxongit.yaml` file, users need to start their runs with `--git-preset` and/or `--git-revision`.

> **Note**: For more information, please run `polyaxon run --help`

### Customize the git preset

The `polyaxongit.yaml` contains a [V1Init](/docs/core/specification/init/) schema definition, users can create the file or customize it manually using an IDE, as long as the content of the file respects the schema.

For example to add some git flags:

```yaml
connection: GIT_CONNECTION_NAME
git: {flags: [--experimental-fetch, --depth 1]}
``` 

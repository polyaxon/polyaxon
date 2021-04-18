---
title: "How to upload artifacts"
sub_link: "how-tos/upload-artifacts"
meta_title: "A guide on how to upload artifacts for your operations - Core Concepts"
meta_description: "Polyaxon run and ops allow to upload artifacts in a completely versioned way."
is_index: true
visibility: public
status: published
tags:
  - concepts
  - tutorials
sidebar: "intro"
---

## Overview

Polyaxon users will often need to upload some artifacts, code, or small dataset before starting an operation 
or might need to attach additional artifacts during the progress of an interactive session or after a run is finished.

If you are dealing with large datasets, we recommend that you host those datasets directly on the data store or the connection and not use Polyaxon CLI for uploading them.

The upload command is meant to provide a fairly simple and effective way of initializing or attaching artifacts that are specific to a single operation.
Since the upload command hosts the data under the run's hash in the artifacts store, the artifacts are automatically versioned and you can upload different versions for each run. Users can also view the artifacts interactively using Polyaxon UI under the artifacts tab.

Polyaxon provides two commands to upload artifacts.

### Run command

This is useful to upload artifacts before starting a run.

To just trigger the default upload behavior, you can use the flag argument: 

```bash
polyaxon run ... -u/--upload
```

To control where the upload manager should set the artifacts under the run's artifacts path: 

```bash
polyaxon run ... -u-to/--upload-to subpath/to/use
```

> **Note**: By default, The upload manager uses a subpath under the run's artifacts root, but you can use `/` to upload the artifacts and place all folders under root without creating an initial subpath.

To use a different path other than the working directory:

```bash
polyaxon run ... -u-from/--upload-from subpath/to/use
```

To control both where and to

```bash
polyaxon run ... -u-from/--upload-from local/subpath/to/use -u-to/--upload-to remote/relative/subpath/to/use
```

> For more details about this command please run `polyaxon run --help`, or check the [command reference](/docs/core/cli/run/)

### Ops command

Similar to the run command, it's possible to attach additional artifacts to a specific run during its progress or after it's done:

```bash
polyaxon ops [-uid] upload
```

Or

```bash
polyaxon ops [-uid] upload --path-to
```

Or

```bash
polyaxon ops [-uid] upload --path-from
```

> For more details about this command please run `polyaxon ops upload --help`, or check the [command reference](/docs/core/cli/ops/#ops-upload)

## Ignore manager

Please note that whenever a user triggers an upload mechanism, Polyaxon CLI or Client will check if the working directory is initialized with a `.polyaxonignore` file. 
If it's the case, it will invoke the ignore manager to check the defined patterns to ignore while traversing the directory's tree.
If no ignore file is found, Polyaxon will ignore by default some predefined patterns.

Users can add the `.polyaxonignore` file to their git repo, or they can create a new project with the `--init` flag, or manually initialize a project using the command `polyaxon init`.

> For more details about this command please run `polyaxon init --help`, or check the [command reference](/docs/core/cli/init/)

## Downloading the artifacts for a specific run

You can always recover all or a subset of the artifacts for a specific operation by using

```bash
polyaxon ops artifacts
```

> For more details about this command please run `polyaxon ops artifacts --help`, or check the [command reference](/docs/core/cli/ops/#ops-artifacts) 

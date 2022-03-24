---
title: "How to upload artifacts"
sub_link: "cli/artifacts-upload"
meta_title: "How to upload artifacts - Core Concepts"
meta_description: "Polyaxon run and ops allow to upload artifacts in a completely versioned way."
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

Polyaxon users will often need to upload some artifacts, code, or small dataset before starting an operation 
or might need to attach additional artifacts during the progress of an interactive session or after a run is finished.

If you are dealing with large datasets, we recommend that you host those datasets directly on the data store or the connection and not use Polyaxon CLI for uploading them.

The upload command is meant to provide a fairly simple and effective way of initializing or attaching artifacts that are specific to a single operation.
Since the upload command hosts the data under the run's hash in the artifacts store, the artifacts are automatically versioned and you can upload different versions for each run.
Users can also view the artifacts interactively using Polyaxon UI under the artifacts tab.

Polyaxon provides two commands to upload artifacts.

> **Note**: Please make sure to check the [ignore behavior](/docs/core/cli/ignore/) to understand how to ignore partterns under the directory you are uploading.

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

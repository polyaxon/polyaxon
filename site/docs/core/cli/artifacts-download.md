---
title: "How to download artifacts"
sub_link: "cli/artifacts-download"
meta_title: "How to download artifacts - Core Concepts"
meta_description: "Polyaxon ops allow to download all artifacts or specific paths, or download artifacts based on their reference."
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

Polyaxon users will often need to download some artifacts previously uploaded or generated during the runtime of an operation.

Polyaxon CLI allows to download the full artifacts of an operation, or a subpath (file or directory), or download artifacts based on their lineage reference.

> For more details about this command please run `polyaxon ops artifacts --help`, or check the [command reference](/docs/core/cli/ops/#ops-artifacts)

## Downloading all artifacts for a specific run

To download all artifacts

```bash
polyaxon ops artifacts [-p] [-uid] [--path-to]
```

## Downloading specific artifacts by path

 * To download a specific file you can use `-f, --file` 

```bash
polyaxon ops artifacts --file path/to/file [-p] [-uid] [--path-to]
```

* To download a specific directory recursively `-d, --dir`

```bash
polyaxon ops artifacts --dir path/to/dir [-p] [-uid] [--path-to]
```


## Downloading specific artifacts by lineage reference

 * To download artifacts by their lineage reference name you can use `-l-name, --lineage-name`

```bash
polyaxon ops artifacts -l-name my-model [-p] [-uid] [--path-to]
```

* To download all artifacts by a specific lineage reference kind you can use `-l-kind, --lineage-kind` 

```bash
polyaxon ops artifacts -l-kind metric [-p] [-uid] [--path-to]
```


---
title: "How to restart runs with different names"
sub_link: "cli/restart-with-different-names"
meta_title: "How to restart runs with different names - Core Concepts"
meta_description: "A guide on how to use Polyaxon CLI to restart runs with different names, descriptions and tags."
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

Users can restart operation with the same initial configuration, oftentimes they might want to restart a run with different names, descriptions and/or tags.

## Passing custom name, description, and tags

In order to provide a custom name

```bash
polyaxon ops restart -uid UUID --name new-run
```

```bash
polyaxon ops restart -uid UUID --name new-run --description adding-some-changes -u -l
```

```bash
polyaxon ops restart -uid UUID --name another-name --description run-with-custom-connection --tags tests,debug
```


> For more details about this command please run `polyaxon ops restart --help`, or check the [command reference](/docs/core/cli/ops/#ops-restart) 

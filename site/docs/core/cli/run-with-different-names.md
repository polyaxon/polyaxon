---
title: "How to start runs with different names"
sub_link: "cli/run-with-different-names"
meta_title: "How to start runs with different names - Core Concepts"
meta_description: "A guide on ow to use Polyaxon CLI to schedule runs with different names, descriptions and tags."
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

Polyaxonfiles can have names, descriptions, and tags both on the component level and on the operation level to override the component values.
When scheduling files with Polyaxon CLI, whether they contain a component or an operation, 
users might want to schedule a run with different names, descriptions and/or tags. Instead of manually opening the file and changing the values, saving the file, closing the file, 
and then executing the run command, users can pass those values directly via the CLI.  

## Passing custom name, description, and tags

In order to provide a custom name

```bash
polyaxon run -f ... --name new-run
```

```bash
polyaxon run -f ... --name new-run --description adding-some-changes -u -l
```

```bash
polyaxon run -f ... --name another-name --description run-with-custom-connection --tags tests,debug
```


> For more details about this command please run `polyaxon run --help`, or check the [command reference](/docs/core/cli/run/) 

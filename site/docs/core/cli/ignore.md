---
title: "Ignore Patterns"
sub_link: "cli/ignore"
meta_title: "A guide on how to set a custom ignore file for Polyaxon CLI - Core Concepts"
meta_description: "Polyaxon upload commands respect an ignore file that contains list of patterns while traversing the directory tree."
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

Please note that whenever a user triggers an upload mechanism, Polyaxon CLI or Client will check if the working directory is initialized with a `.polyaxonignore` file.

## Default behavior

If a user does not define a custom `.polyaxonignore`, the CLI will use a default list of patterns to avoid uploading some common ignorable files and dirs by default.
For example Polyaxon CLI will skip uploading the `.git` folder. 

## Ignore manager

Every time an upload command is invoked it will invoke the ignore manager to check the defined patterns to ignore while traversing the directory's tree.
 

## Defining a custom ignore file

Users can add the `.polyaxonignore` file to their git repo, or they can create a new project with the `--init` flag, or manually initialize a project using the command `polyaxon init`.

> For more details about this command please run `polyaxon init --help`, or check the [command reference](/docs/core/cli/init/)

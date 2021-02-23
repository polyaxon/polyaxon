---
title: "IDE Set-Up on VSCode"
meta_title: "IDE Set-Up on VSCode"
meta_description: "How to validate Polyaxonfiles (YAML) against the JSON Schema on VSCode"
custom_excerpt: "Polyaxon provides a JSON Schema that enables validation of YAML resources in your VSCode IDE."
image: "../../content/images/integrations/vscode.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - ide
featured: false
popularity: 0
visibility: public
status: published
---

How to validate Polyaxonfiles (YAML) against the JSON Schema on VSCode.

## Overview

Polyaxon provides a JSON Schema that enables validation of YAML resources in your VSCode IDE.

## Install Red Hat YAML plugin

In VSCode, you can use Red Hat YAML plugin, it provides error highlighting and auto-completion for Polyaxonfiles.

![vscode-yaml-completion](../../content/images/integrations/ide/vscode-yaml-plugin.png)

## Configuration

Open the YAML schemas settings:

![vscode-yaml-settings](../../content/images/integrations/ide/vscode-yaml-settings.png)

Configure your IDE to reference Polyaxonfile's schema:

![vscode-yaml-configure](../../content/images/integrations/ide/vscode-yaml-configure.png)

The schema is located at [https://raw.githubusercontent.com/polyaxon/polyaxon/master/sdks/jsonschema/v1/polyaxonfile.schema.json](https://raw.githubusercontent.com/polyaxon/polyaxon/master/sdks/jsonschema/v1/polyaxonfile.schema.json).
 
We recommend to use a file glob pattern that is specific to your Polyaxonfiles, for example:
 * `polyaxonfile*.yaml`: All files that start with `polyaxonfile` and end with `.yaml`.
 * `polyaxonfiles/**/*.yaml`: All files located under `polyonaxfiles` path.

## Restart the IDE to use the completion and validation

After configuring the IDE correctly, if you open a polyaxonfile you should see a smarter behaviour, including type errors and context-sensitive autocomplete.

![vscode-yaml-completion1](../../content/images/integrations/ide/vscode-yaml-completion.png)

> **Note**: the completion on VSCode has still some issue under the run section.

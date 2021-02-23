---
title: "IDE Set-Up on IntelliJ IDEA"
meta_title: "IDE Set-Up on IntelliJ IDEA (PyCharm, ...) (Community & Ultimate Editions)"
meta_description: "How to validate Polyaxonfiles (YAML) against the JSON Schema on IntelliJ IDEA (PyCharm, ...)"
custom_excerpt: "Polyaxon provides a JSON Schema that enables validation of YAML resources in your IntelliJ IDEA (PyCharm, ...) IDE."
image: "../../content/images/integrations/ide-intellij.png"
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

How to validate Polyaxonfiles (YAML) against the JSON Schema on IntelliJ IDEA (PyCharm, ...).

## Overview

Polyaxon provides a JSON Schema that enables validation of YAML resources in your IntelliJ IDEA (PyCharm, ...) IDE.
In all IntelliJ IDEA editions, YAML validation is supported natively.

## Configuration

Configure your IDE to reference Polyaxonfile's schema:

![intellij-configure](../../content/images/integrations/ide/intellij-configure.png)

The schema is located at [https://raw.githubusercontent.com/polyaxon/polyaxon/master/sdks/jsonschema/v1/polyaxonfile.schema.json](https://raw.githubusercontent.com/polyaxon/polyaxon/master/sdks/jsonschema/v1/polyaxonfile.schema.json).
 
We recommend to use a file glob pattern that is specific to your Polyaxonfiles, for example:
 * `polyaxonfile*.yaml`: All files that start with `polyaxonfile` and end with `.yaml`.
 * `polyaxonfiles/**/*.yaml`: All files located under `polyonaxfiles` path.

## Restart the IDE to use the completion and validation

After configuring the IDE correctly, if you open a polyaxonfile you should see a smarter behaviour, including type errors and context-sensitive autocomplete.

![intellij-completion1](../../content/images/integrations/ide/intellij-completion.png)

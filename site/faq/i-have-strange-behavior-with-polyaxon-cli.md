---
title: "I have a strange behavior with Polyaxon CLI."
meta_title: "Please make sure you have the latest Polyaxon CLI, you can check your CLI version using `polyaxon version --check` - FAQ"
meta_description: "Please make sure you have the latest Polyaxon CLI, you can check your CLI version using `polyaxon version --check`"
featured: false
custom_excerpt: "Please make sure you have the latest Polyaxon CLI, you can check your CLI version using `polyaxon version --check`"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - cli
---

Please make sure you have the latest Polyaxon CLI, you can check your CLI version using `polyaxon version --check`.

Make sure you don't have the legacy CLI installed, if you run `pip freeze | grep polyaxon` and get any of the following libraries:
 * polyaxon-client
 * polyaxon-cli
 * polyaxon-schemas
 * polyaxon-deploy
 * polyaxon-dockerizer
 
Uninstall the legacy packages: `pip uninstall polyaxon-client polyaxon-cli ...`


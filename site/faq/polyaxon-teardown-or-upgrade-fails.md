---
title: "I’m getting (Error: uninstall: Release not loaded: polyaxon: release: not found)"
meta_title: "I’m getting (Error: uninstall: Release not loaded: polyaxon: release: not found) - FAQ"
meta_description: "All Polyaxon admin commands accept a -f/--file argument for specifying the configuration to deploy/upgrade/teardown."
featured: false
custom_excerpt: "All Polyaxon admin commands accept a -f/--file argument for specifying the configuration to deploy/upgrade/teardown."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - api
---

Polyaxon uses some default values for deploying and managing Polyaxon deployment.

if you used a custom config with specific values that diverge from the default values, you will need to pass the config file to all these commands to construct a full context of your deployment.

All Polyaxon admin commands accept a -f/--file argument for specifying the configuration to deploy/upgrade/teardown.

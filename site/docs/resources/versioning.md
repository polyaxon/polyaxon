---
title: "Polyaxon Versioning"
sub_link: "versioning"
meta_title: "Polyaxon Versioning - Polyaxon Semantic Versioning Mechanism"
meta_description: "Polyaxon will be following Semantic Versioning."
visibility: public
status: published
tags:
  - reference
---

> We will update this document to reflect any change in our release mechanism.

Polyaxon is using a SemVer ([Semantic Versioning](https://semver.org/)) for all of its open-source releases — major versions indicate breaking, 
backward-incompatible changes; minor versions mean new features, and patch releases are bug fixes only.

## Benefits

 * Host and support several versions of semantically contained documentation resources.
 * Every time a new release is created with the PATCH change, users should assume a completely backwards-compatible upgrade.
 * Every time a new migrations (data and db) is introduced, the MINOR version will be bumped while providing automatic migration paths.
 * Every time a new compatible feature or functionality is released, the MINOR version will be bumped.

## Release cycles

New versions will be released:

  * Whenever a major regression, bug, or security fix is made.
  * Whenever a new improved functionality is developed and tested on different infrastructures.
  * Every 2 weeks/month depending on the scope of the features being developed. 

## Other components

In addition to Polyaxon's core functionality, we develop several other aspects and components that we believe have a major impact on the productivity of our users. 
These components will be marked separately with alpha/beta until they reach a stable state.

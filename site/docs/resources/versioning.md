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

Polyaxon is using SemVer ([Semantic Versioning](https://semver.org/)) for all of its open-source releases:
 * Major numbers indicate breaking, backward-incompatible changes, or substantial project milestones.
 * Medium numbers indicate new features, may include API changes with possible deprecations, release notes must be read carefully before upgrading between medium point releases.
 * Minor numbers indicate patches, bug fixes, enhancements and feature improvements only.

## Benefits

 * Host and support several versions of semantically contained documentation resources.
 * Clear migration paths.

## Release cycles

New versions will be released:

  * Whenever a major regression, bug, or security fix is made.
  * Whenever a new improved functionality is developed and tested on different infrastructures.
  * Every week/2 weeks/month depending on the scope of the features being developed.

## Other components

In addition to Polyaxon's core functionality, we develop several other aspects and components that we believe have a major impact on the productivity of our users.
These components will be marked separately with alpha/beta until they reach a stable state.

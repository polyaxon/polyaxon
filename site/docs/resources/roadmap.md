---
title: "Product Roadmap"
sub_link: "roadmap"
meta_title: "Product Roadmap - Polyaxon Product Roadmap and Highlights"
meta_description: "Please note that the roadmap is intended to provide high-level visibility into the short-term direction of the product. This can change at any time."
visibility: public
status: published
tags:
  - reference
---

> Please note that the roadmap is intended to provide high-level visibility into the short-term direction of the product. This can change at any time. Several of these aspects are either in alpha phase, private beta, beta, or under heavy development.

## Product Roadmap

This roadmap features several aspects of out product, every aspect has it's own subsection. 
The main and most important aspect of our roadmap is the platform stability.

For features, improvements, and issues that we are currently working on, you can check the latest release with the **[WIP]** tag.
We welcome our users to give feedback and suggest updates and features.

### Create UI launchers

Currently the UI provides an editor to write YAML, by introducing a UI launcher we can improve the user experience and simplify creating new operations.
There are two use case for the launchers:
 1. Components saved in the public or private hub have inputs and outputs definition, the launcher should be able to parse those sections and provide the necessary forms for users to fill params to start operations.
 2. Authoring operations from scratch, the launcher should provide a simple form to fill-in the basic container sections, i.e. image, command, args, and resources. 

### Add UI auto-completion 

The YAML editor in the UI should be able to parse, lint, and provide auto-completion based on Polyaxon specification. 

### Improve graphs and charts experience

Several users have requested some kind of storage capabilities to preserve the a dashboard schema and history, this can be done using the URL query params.

### Allow multi-section dashboards

This is a feature that make sense both for single run and multi-run dashboards, where sections can be folded or expanded, and can help users organize their dashboards.

### Improve search experience

Similar to the charting enhancement, the URL query params could be used as the state handler for the search, which should also provide several features like history and url sharing.

### Enable hooks and per-operation-build on Polyaxon CE

In order to enable these features we need to add the run edge table to Polyaxon CE to reuse the logic already implemented in the commercial version.

### Enable an agent-based workflow on Polyaxon CE 

Similar to the previous point, by enabling an agent-based workflow on Polyaxon CE, we can expose some new features like concurrency and global queue on Polyaxon CE.
Other features like batch deletion and batch notifications can be enabled for Polyaxon CE as well.

Polyaxon CE also has some known limitations with its reconciliation logic because there's no queue concept to check for events acknowledgement.

---
title: "Roadmap"
sub_link: "roadmap"
code_link: "releases/roadmap.md"
meta_title: "Polyaxon Roadmap and upcoming release notes - Polyaxon Releases"
meta_description: "Polyaxon roadmap, release notes, migrations, and deprecation notes."
visibility: public
status: published
tags:
  - reference
sidebar: "releases"
---

## Roadmap

### Sandbox

 * **Beta**: A new sandbox debugger for running and visualizing on a local machine without any docker requirement.

### Core

 * **Enhancement**: Add mid-runtime update with `apply` logic.

### CLI
 ...

### Agent

 * **New**: (Beta) Add cluster and namespace monitoring:
   * Show nodes's states and health.
   * Show nodes's CPU/Memory/GPU consumption.

### Client

 * **New**: Add `@component` decorator to allow declaring components based on Python functions.
   * Polyaxon CLI will automatically generate a CLI based the decorator which will allows users to reduce the boilerplate and leverage their functions directly without having to use `click` or `argparse`.
   * The decorator automatically detects `NO_OP` and becomes a pass-through.
 * **New**: Add `@op/@operation` decorator to allow invoking components programmatically.
   * The decorator automatically detects `NO_OP` and defaults to a local python function call.
 * **New**: Add support for Python type hints in the both the class and the decorator component declarations. 
 * **New**: Automatically detect if the filesystem should use the stream or the artifacts store directly.

### Specification

 * **New**: (Beta) Multi-container pipeline orchestration in a single operation.
 * **Enhancement**: Allow setting DAG outputs without the SDK/Client.

### UI

 * **New**: Add new advanced filters, allow filtering the runs in the comparison table based on:
   * parallel coordinate.
   * histogram.
   * activity calendar.
   * custom visualizations.
 * **New**: Allow comparing resources with metrics and cross runs resources.
 * **New**: Add predefined hyperparameter tuning widgets/visualizations.
 * **New**: When possible, the `?` will show a direct link to the docs relevant to the UI current page. e.g. if the user is on the service accounts setting tab the `?` will have a link to the guides related to the service accounts.
 * **New**: Data table widget for rendering multi-step events in addition to the per-step slider widget for:
   * audio events.
   * video events.
   * image events.
   * histogram events.
 * **Enhancement**: Allow visualizing multiple images (index range) at the same time.
 * **Enhancement**: Implement lazy loading of widgets in dashboards based on their visibility in viewport.
 * **Enhancement**: Do not render large artifacts and provide preview button.
 * **Fix**: Issue with heat fields not persisted with saved queries.

### Tracking

 * **New**: Add support for logging data versions, summaries, reports, and quality.
 * **New**: Add log table.
 * **New**: Add custom bar plots.
 * **Enhancement**: Allow tracking dataframes as parquet files.

### Commercial

 * **New**: Add notification center to allow users to control and manage notifications using the UI.
 * **New**: Add selection reports, this is similar to selection in v0 but the new implementation will support all the new features and dashboard flexibility (events, artifacts, lineages, comparison, custom columns selection, multi-field sorting, ...):
   * Allows adding single runs to a report from the run's overview page.
   * Allows adding multiple runs to a report using a multi-run action.
   * Add project sidebar button `Reports`.
   * Allow running downstream-ops for a report, e.g. multi-run Tensorboard.
 * **New**: Add project contributors on the overview page to show all members who contributed to a specific project.
 * **Beta**: Add new queuing logic:
    * fair-share queuing
    * auto-preemption based on priority
    * auto-requeueing for suspended operations
    * per-queue preset
 * **Enhancement**: Allow owner/billing users to reset the billing anchor date, several users asked to change when they get billed during month.
 * **Enhancement**: Add possibility to save searches on the global runs table.
 * **Enhancement**: Add possibility to save custom analytics searches.
 * **Enhancement**: Add more informative messages and handling when scaling down usage/agents/seats or when downgrading to a plan missing a specific feature.
 * **Enhancement**: Add support for resuming pipelines and matrix operations.
 * **Enhancement**: Improve resuming or restarting an operation that is part of a pipeline.
 * **Enhancement**: Investigate the new `suspend` feature to provide immediate concurrency change instead of the current [draining logic](/faq/How-does-changing-concurrency-work/).
 * **Fix**: Regression in metric early stopping policies.

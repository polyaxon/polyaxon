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

### Core
 
 * **New**: Add support for annotations in the connections specification.
 * **Enhancement**: Improve upload logic when streams service is configured with multiple replicas.
 * **Enhancement**: Add mid-runtime update with `apply` logic.
 * **Fix**: Issue with unit sanitization and prevent compiler from raising an error.  

### Sidecar

 * **Enhancement**: Improve the artifacts syncing logic to be more resilient to failed requests or intermittent errors.

### CLI
 
 * **New**: Add `polyaxon ops shell` command similar to the shell tab.
 * **Enhancement**: Collect `hash` information for uploaded artifacts in the lineage metadata.

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

### Specification

 * **New**: (Beta) Multi-container pipeline orchestration in a single operation.
 * **Enhancement**: Allow setting DAG outputs without the SDK/Client.

### UI

 * **New**: Add operation status color indicator to the page's favicon.
 * **New**: Add markdown, scalar, summary, lineage, and performance widgets.
 * **New**: Add Metrics/Params correlation and importance.
 * **New**: Add new advanced filters, allow filtering the runs in the comparison table based on:
   * parallel coordinate.
   * histogram.
   * activity calendar.
   * custom visualizations.
 * **New**: Allow comparing resources with metrics and cross runs resources.
 * **New**: Add predefined hyperparameter tuning widgets/visualizations.
 * **New**: Allow inspecting charts and showing the data used.
 * **Enhancement**: Allow visualizing multiple images (index range) at the same time.
 * **Enhancement**: Implement lazy loading of widgets in dashboards based on their visibility in viewport.
 * **Enhancement**: Do not render large artifacts and provide preview button.
 * **Enhancement**: Improve logs viewer to better handle long log lines.
 * **Enhancement**: Add missing `id` / `uid` / `uuid` from the search suggestions.
 * **Enhancement**: Issue with new dashboard sections minimized by default.

### Tracking

 * **New**: Add support for logging data versions, summaries, reports, and quality.
 * **Enhancement**: Re-enable histogram logging.

### Hub

 * **New**: Add DVC(data version control) integration.

### Commercial

 * **New**: Add global search (cmd + k), a single global search field to provide easy access to:
   * Projects
   * Models
   * Components
   * Connections
   * Operations
 * **New**: Add notification center to allow users to control and manage notifications using the UI.
 * **New**: Add selection reports, this is similar to selection in v0 but the new implementation will support all the new features and dashboard flexibility (events, artifacts, lineages, comparison, custom columns selection, multi-field sorting, ...):
   * Allows adding single runs to a report from the run's overview page.
   * Allows adding multiple runs to a report using a multi-run action.
   * Add project sidebar button `Reports`.
   * Allow running downstream-ops for a report, e.g. multi-run Tensorboard.
 * **New**: Add project contributors on the overview page to show all members who contributed to a specific project.
 * **Enhancement**: Allow owner/billing users to reset the billing anchor date, several users asked to change when they get billed during month.
 * **Enhancement**: Improve UI to support redirection to the original page after authentication.
 * **Enhancement**: Add possibility to save searches on the global runs table.
 * **Enhancement**: Add possibility to save custom analytics searches.
 * **Enhancement**: Add more informative messages and handling when scaling down usage/agents/seats or when downgrading to a plan missing a specific feature.
 * **Enhancement**: Add support for resuming pipelines and matrix operations.
 * **Enhancement**: Improve resuming or restarting an operation that is part of a pipeline.
 * **Enhancement**: Improve Tags API and UI.
 * **Enhancement**: Investigate the new `suspend` feature to provide immediate concurrency change instead of the current [draining logic](/faq/How-does-changing-concurrency-work/).
 * **Fix**: Regression in metric early stopping policies.

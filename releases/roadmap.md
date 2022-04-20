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

## Next Release V1.18.0

> **Note**: This minor version is WIP and not released yet.

### CLI

 * **Enhancement**: Collect `hash` information for uploaded artifacts in the lineage metadata.

### Core

 * **New**: Add support for annotations in the connections specification.
 * **Enhancement**: Migrate hyperparameter tuning and tracking modules to separate repos.
 * **Enhancement**: Improve query manager to return distinct values.

### Client

 * **New**: Add promote method to a model version or artifact version directly from the `RunClient`:
   * `RunClient.promote_to_model_version` this is similar to `ProjectClient.register_model_version` but directly from the run client instance.
   * `RunClient.promote_to_artifact_version` this is similar to `ProjectClient.register_artifact_version` but directly from the run client instance.
 * **New**: Add `get_runs_artifacts_lineage` to `RunClient` to allow listing artifacts lineage information from multiple runs under the same project based on a query specification.
 * **New**: Add new `OrganizationClient`, this client will only be accessible to users with enough permissions or it will raise 401/403 errors:
    * Allows listing and interacting with agents.
    * Allows listing and interacting with connections.
    * Allows listing projects.
    * Allows listing cross project runs.

### Operator

 * **Enhancement**: Update training operator to use the newest Kubeflow release.

### Query Language

 * **New**: Allow filtering by connections:
    * By name `connections.name: CONNECTION1 | CONNECTION2`
    * By tag `connections.tags: TAG1 | TAG2`
    * By kind `connections.kind: git`
 * **New**: Allow filtering by artifacts lineage:
    * By name `artifacts.name: LINEAGE1 | LINEAGE2`
    * By kind `artifacts.kind: model`
    * By path `artifacts.path: foo/bar`
    * By state `artifacts.state: STATE`

### Tracking

 * **New**: Allow to specify the connection name when logging assets and artifacts to associate the lineage to a specific connection.
 * **Enhancement**: Improve logic around assets and artifacts logging to only trigger versioned behavior (step-wise) when a step parameter is provided.
 * **Enhancement**: Improve outputs state calculation.

### Streams

 * **New**: Add support for multi-connections:
   * Possibility to mount multiple volumes to upload and download artifacts to and from connections other than the artifacts store.
 * **Enhancement**: Improve k8s connections and handling.
 * **Enhancement**: Update fs backends.

### UI

 * **New**: Add operation status color indicator to the page's favicon.
 * **New**: Add markdown, scalar, summary, lineage, and performance widgets.
 * **New**: Add Metrics/Params correlation and importance.
 * **New**: Show an indicator on artifacts lineage if it's promoted to a model version or artifact version.
 * **New**: Add connection information to artifacts lineage.
 * **Enhancement**: Update the queues table with a link next to each queue to filter all runs by a specific queue.
 * **Enhancement**: Update the connections table with a link next to each connection to filter all runs by a specific connection.
 * **Enhancement**: Show artifact' state on the lineage tables.
 * **Enhancement**: Keep configuration of logs, artifacts, and dashboards tabs unchanged when changing tabs of the same run.
 * **Enhancement**: Improve queues usage to remove `.0` in the denominator.
 * **Fix**: Typo in tip for registering component/model/artifact versions.
 * **Fix**: Regression in multi-run scatter plot.

### Hub

 * **New**: Add DVC(data version control) integration.
 * **New**: Add support for ssh connection to allow connecting VSCode and Pycharm.

### Docs

 * **Enhancement**: Improve navigation and provide short-cuts.
 * **Enhancement**: Improve `ProjectClient` and `RunClient` reference docs.
 * **Enhancement**: Add new intro tutorial about registering components, models, and artifacts.
 * **Fix**: Edit links to point to the correct code files.

### Deployment

 * **Security**: Fix CVE issues.

### Commercial

 * **New**: Project and organization info pages redesign.
 * **New**: Add support for readme on component/model/artifact versions.
 * **New**: Add cross-projects artifact/component/model versions view similar to `All Runs`.
 * **New**: Add a new tab to explore unregistered artifact/component/model versions under each project. 
 * **New**: Allow getting a connection's schema by name.
 * **Enhancement**: Improve operations in DAGs with pending approval and upstream failures.
 * **Enhancement**: Reduce member roles confusion:
   * Add a note to `admin` to emphasize that is a `Project admin`.
   * Add a note to `manager` to emphasize that is a `Organization admin`.
 * **Enhancement**: Improve compilation process to better handle converting artifact lineage, model, and artifact versions references.

## Short Term Roadmap

### CE

 * **New**: Add support for agent based deployment.

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

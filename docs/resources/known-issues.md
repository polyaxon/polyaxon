---
title: "Polyaxon known issues and limitations"
sub_link: "known-issues"
meta_title: "Polyaxon known issues and limitations - Polyaxon Resources"
meta_description: "Polyaxon known issues, regressions, bugs, limitations, and their update status."
visibility: public
status: published
tags:
    - reference
---

The content of this page is intended to keep users up-to-date about the issues, limitations, bugs fixed, WIP, or still unsolved in a given version.

Every bug fixed will be mentioned here with a link to github, if available, and an updated status, i.e. fixes for known issues in 0.4 series and that will be available in 0.5 series.

> N.B. this page does not intend to list every github issue, but only those that impact a stable usage of the platform.


### Add a warning when code is big

[Github: #229](https://github.com/polyaxon/polyaxon/issues/229) -> fixed.

### Make .polyaxonignore honour .gitignore syntax

[Github #306](https://github.com/polyaxon/polyaxon/issues/306) -> fixed.

### File view does not keep tabs

[Github #433](https://github.com/polyaxon/polyaxon/issues/433) -> open

### Horovod Backend doesn't pass the environmental variables to workers

[Github #429](https://github.com/polyaxon/polyaxon/issues/429) -> open

### Helm chart does not work correctly when RBAC is disabled

This is issue is noticed in Minikube because start the cluster with RBAC disabled (`No github issue`) -> fixed

### Polyaxon cannot be installed with latest helm version

[Github #455](https://github.com/polyaxon/polyaxon/issues/455) -> Fixed

### Default build backend was ignored in some instances

[Github #457](https://github.com/polyaxon/polyaxon/issues/457) -> Fixed

### Support latest version of jupyter lab

[Github #422](https://github.com/polyaxon/polyaxon/issues/422) JupyterLab cannot resolve some paths, namely the css/theme path. -> Fixed

### Update redis chart and support using external/managed redis instance

Polyaxon has a new up-to-date version of the stable redis chart, and it supports using an external managed redis instance -> fixed.

### Update rabbitmq chart and support using external/managed rabbitmq instance

Polyaxon has a new up-to-date version of the stable rabbitmq-ha chart, and it supports using an external managed rabbitmq instance -> fixed.

### Allow to specify a service account for jobs/experiments

[Github #447](https://github.com/polyaxon/polyaxon/issues/447) The env section will allow to pass in a custom SA, 
as well as a config to override default SA for experiments/jobs/builds/... A documentation ref will be published with the minimum RBAC access required -> Fixed

---
title: "Builds"
sub_link: "builds"
meta_title: "Polyaxon builds - Polyaxon Automation Reference"
meta_description: "Use Polyaxon to trigger per-operation build process to automate the containerization of dynamic environments."
visibility: public
status: published
is_index: true
tags:
  - reference
  - polyaxon
  - polyflow
sidebar: "automation"
---

<blockquote class="info">This feature is still in Beta and requires v1.9.2 or higher!</blockquote>

## Overview

Polyaxon provides a build section on the component/operation level to automatically trigger a per-run build process and create containers for dynamic environments.


## Use cases

Users can define a build process or attach a build preset:

 * To dynamically create new containers before starting the main operation or the hyperparameter tuning process.
 * To automate the process of building fast changing and dynamic environments.
 * To package different requirements, artifacts, and code in a single container.
 * To quickly test new configurations before building a stable image.

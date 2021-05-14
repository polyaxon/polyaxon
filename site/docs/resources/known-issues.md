---
title: "Known issues and limitations"
sub_link: "known-issues"
meta_title: "Known issues and limitations - Polyaxon Resources"
meta_description: "Polyaxon known issues, regressions, bugs, limitations, and their update status."
visibility: public
status: published
tags:
  - reference
---

> N.B. this page does not intend to list [github issues](https://github.com/polyaxon/polyaxon/issues?q=is%3Aopen+is%3Aissue+label%3Abug).

The content of this page is intended to keep users up-to-date about the issues, limitations, bugs fixes that are WIP or still unsolved.

### Early stopping policies  

The scheduling logic for early stopping [policies](https://polyaxon.com/docs/automation/helpers/early-stopping/#policy) was deactivated after making tuners fully customizable.
Users can still use both status-based and metric-based early stopping strategies, but they cannot set the policy.

We intend to reactivate the logic in the coming weeks.

### Hyperopt search manager

A bug was introduced to the hyperopt search manager and does not correctly schedule jobs. We intend to fix this issue in the next few weeks.

### Graph view

The graph view does not render correctly on Safari, this is currently a known issue, and the solution that we intend to make is to reduce the amount of HTML rendered in each node and only focus on SVG,
this change should also improve the rendering speed of large graphs. 

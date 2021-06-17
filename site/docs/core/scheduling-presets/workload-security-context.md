---
title: "Workload Security Context"
sub_link: "scheduling-presets/workload-security-context"
meta_title: "Workload Security Context - scheduling presets"
meta_description: "Setting a default workload security context using presets."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

By default, Polyaxon operations run without a security context, and pods run as root. 
Sometimes you might even need to run pods with privileged security, for examples the `dockerizer` component.

## Defining a security context preset

If you need to configure a security context for your jobs and services, you can use the [environment.SecurityContext](/docs/core/specification/environment/#securitycontext) section:

```yaml
runPatch:
  environment:
    securityContext:
    runAsUser: 2222
    runAsGroup: 2222
    runAsNonRoot: true
```

By [saving this preset](/docs/management/organizations/presets/) as `security-context`, users can now use this section in their jobs or services automatically:

```bash
polyaxon run ... --presets=security-context
```

You can also use the preset directly on the component or operation definition:

```yaml
kind: operation
presets: [security-context]
...
```

## Global or per project security context

Managers and Admins of Polyaxon organizations and projects can set the security context directly as the default preset.

Setting the organization's default preset:

![default-org-preset](../../../../content/images/dashboard/presets/default-org-preset.png)

Setting a project's default preset:

![default-project-preset](../../../../content/images/dashboard/presets/default-project-preset.png) 

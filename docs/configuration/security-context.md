---
title: "Security context configuration"
sub_link: "security-context"
meta_title: "Security context configuration in Polyaxon - Configuration"
meta_description: "Polyaxon's Security context configuration for containers."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - security
sidebar: "configuration"
---

Polyaxon runs all containers as root by default, this configuration is often fine for several deployment, 
however, in some use case it can be expose a compliance issue for some teams.

Polyaxon provides a simple way to enable a security context for all core components, experiments and jobs.  

## Default configuration

```yaml
securityContext:
  enabled: false
  user: 2222
  group: 2222
```

## Enable security context

```yaml
securityContext:
  enabled: true
```

or enable with custom UID/GID other than 2222/2222:

```yaml
securityContext:
  enabled: true
  user: 1111
  group: 1111
```

This will enable a security context to run all containers using a UID/GID == 1111/1111.

## Allow the UID/GID to access repos, outputs, logs and any data with write mode

To allow the platform to function correctly you need to make sure that a process running 
in a container with security context has rights to read/write git repos, outputs, and logs.

For example, if you use this path `/polyaxon-outputs` as your outputs, you can run:

```bash
chown -R 2222:2222 /polyaxon-outputs
```

Same thing for the repos mount path and logs mount path. Otherwise you might have issues:

 * Uploading code or cloning external repos.
 * Running experiments/jobs saving outputs
 * Collecting logs

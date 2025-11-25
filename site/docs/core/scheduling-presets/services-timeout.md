---
title: "Services Timeout"
sub_link: "scheduling-presets/services-timeout"
meta_title: "Services Timeout - scheduling presets"
meta_description: "Cleaning Jupyter notebooks and Tensorboard session automatically with a timeout preset."
tags:
  - namespace
  - queueing
  - pipelines
  - kubernetes
  - scheduling
sidebar: "core"
---

## Overview

Polyaxon provides a simple process for spawning and managing Jupyter notebooks, Tensorboard, RStudio, and other services.
Oftentimes, users will start a Tensorboard session or notebook server that requests GPU resources and will forget stopping the service.

As an admin you can create, or even enforce a timeout mechanism, on these type of services using a preset. Polyaxon supports two types of timeout mechanisms:

1. **Absolute timeout**: Services are terminated after a fixed duration regardless of activity
2. **Idle-based culling**: Services are terminated after being inactive/idle for a specified period

## Defining an absolute timeout preset

Defining an absolute timeout preset is straightforward in Polyaxon:

```yaml
termination:
  timeout: 86400 # 24 hours
```

By [saving this preset](/docs/management/organizations/presets/) as `services-timeout-24`,
users can automatically clean their sessions after 24 hours:

```bash
polyaxon run ... --presets=services-timeout-24
```

You can also use the preset directly on the component or operation definition:

```yaml
kind: operation
presets: [services-timeout-24]
...
```

## Defining an idle-based culling preset

For services that may run for long periods but are only actively used occasionally (like Jupyter notebooks), you can configure idle-based culling to automatically stop services when they are not being actively used:

```yaml
termination:
  culling:
    timeout: 3600  # 1 hour of idle time
  probe:
    http:
      path: "/api/status"
      port: 8888
```

This configuration will stop the service after 1 hour of inactivity. The `probe` section defines how to check for activity:

### HTTP Activity Probe

For Jupyter notebooks and JupyterLab:

```yaml
termination:
  culling:
    timeout: 3600  # Stop after 1 hour idle
  probe:
    http:
      path: "/api/status"  # Jupyter API endpoint
      port: 8888           # Default Jupyter port
```

### Exec Activity Probe

For custom services or other applications, you can use an exec probe:

```yaml
termination:
  culling:
    timeout: 7200  # Stop after 2 hours idle
  probe:
    exec:
      command: ["bash", "-c", "check-activity.sh"]
```

The command should return:
- Exit code `0` if there was activity in the last check period
- Exit code `1` if there was no activity

## Combining absolute timeout and culling

You can combine both timeout mechanisms. The service will be stopped when either condition is met (whichever happens first):

```yaml
termination:
  timeout: 86400   # Absolute: stop after 24 hours regardless of activity
  culling:
    timeout: 3600  # Idle: stop after 1 hour of inactivity
  probe:
    http:
      path: "/api/status"
      port: 8888
```

## Example presets

### Jupyter Notebook with 1-hour idle timeout

```yaml
termination:
  culling:
    timeout: 3600
  probe:
    http:
      path: "/api/status"
      port: 8888
```

Save as preset: `jupyter-idle-1h`

### Jupyter Notebook with 4-hour idle timeout and 24-hour absolute timeout

```yaml
termination:
  timeout: 86400
  culling:
    timeout: 14400
  probe:
    http:
      path: "/api/status"
      port: 8888
```

Save as preset: `jupyter-idle-4h-max-24h`

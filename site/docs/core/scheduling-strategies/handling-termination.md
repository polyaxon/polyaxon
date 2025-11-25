---
title: "Handling failures and termination"
sub_link: "scheduling-strategies/handling-termination"
meta_title: "Handling failures and termination - scheduling strategies"
meta_description: "Handling failures and termination and ensuring robust scheduling."
visibility: public
status: published
tags:
  - tutorials
  - concepts
sidebar: "core"
---

It's important to ensure that jobs and services are robust and that they respect SLAs.

Polyaxon exposes a section for handling failure and managing [termination](/docs/core/specification/termination/).

You can set a default termination on the component level and override the values for each operation,
or you can only define termination on some operation without setting too much information on the component.
You can also use the [scheduling presets](/docs/core/scheduling-presets/)
to define one or multiple termination configurations that you can use with one or several of your operations.

## Handling failures with max retries

In order to make your operations resilient to failure that could happen for a variety of reasons:
 * pod preemption, node failure, ...
 * HTTP requests failing when fetching data or assets
 * Service or external API down or unavailable for a short period of time

Polyaxon provides a concept called [max_retries](/docs/core/specification/termination/#maxretries).


## Enforcing SLAs with timeout

It's also important to enforce SLAs (Service Level Agreements) for your operations.
Polyaxon provides the [timeout](/docs/core/specification/termination/#maxretries) section that
will stop a job or service if it does not succeed or terminate on its own during the time window defined in the termination timeout.

Timeout can be combined with hooks/notifications to deliver the necessary information to users or external services.

## Debugging with TTL

The third key in the termination section is [ttl](/docs/core/specification/termination/#ttl).
By default, Polyaxon cleans out and removes all cluster resources as soon as an operation is done.
It is often necessary to keep a job or a service after it's done for sanity checks or debugging purposes.

## Optimizing resource usage with service culling

For long-running services like Jupyter notebooks, Tensorboard, or RStudio, Polyaxon provides an idle-based culling mechanism
that automatically stops services when they are not actively being used. This is particularly useful for:
* Services that request expensive resources (GPUs, high-memory nodes)
* Preventing resource waste from forgotten sessions
* Automatically freeing up cluster capacity for other workloads

Unlike the absolute `timeout` which terminates after a fixed duration regardless of usage,
culling only triggers when the service has been idle for the specified period.

### Configuration

The culling feature is configured through the `termination` section with two key components:

```yaml
termination:
  culling:
    timeout: 3600  # Idle timeout in seconds
  probe:
    http:
      path: "/api/status"
      port: 8888
```

* **`culling.timeout`**: Duration in seconds that the service must be idle before it is terminated
* **`probe`**: Defines how to check for activity (HTTP or Exec)

### How culling works

1. Polyaxon periodically checks the service's activity status using the configured probe
2. If the probe indicates activity, the idle timer resets
3. If no activity is detected for the duration specified in `culling.timeout`, the service is automatically stopped
4. On probe errors, the service is assumed to be active to avoid accidental termination

### Activity probes

The culling feature works by periodically checking for activity using configurable activity probes:

#### HTTP probes

HTTP probes poll a service endpoint to detect activity. The endpoint must return a JSON response with a `last_activity` field containing an RFC3339 timestamp:

```json
{
  "last_activity": "2024-01-15T10:30:00Z",
  "started": "2024-01-15T08:00:00Z"
}
```

Configuration example for Jupyter:

```yaml
termination:
  culling:
    timeout: 3600
  probe:
    http:
      path: "/api/status"  # Default path if not specified
      port: 8888           # Uses first service port if not specified
```

**Common HTTP probe paths:**
* Jupyter/JupyterLab: `/api/status` (port 8888)
* Custom services: Implement an endpoint that returns the `last_activity` JSON field

#### Exec probes

Exec probes run custom commands inside the container to determine activity status:

```yaml
termination:
  culling:
    timeout: 7200
  probe:
    exec:
      command: ["bash", "-c", "/scripts/check-activity.sh"]
```

The command runs in the container's root (`/`) directory. Exit code `0` indicates activity, non-zero indicates idle.

> **Note**: Exec probes are currently defined in the API but not yet fully implemented. Use HTTP probes for production workloads.

### Combining timeout and culling

You can use both absolute timeout and idle-based culling together. The service will be stopped when either condition is met (whichever happens first):

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

This configuration ensures:
* Active services are terminated after 24 hours maximum
* Idle services are terminated after 1 hour of inactivity

### Troubleshooting

If culling is not working as expected:

1. **Verify probe configuration**: Ensure the path and port match your service's activity endpoint
2. **Check endpoint response**: The HTTP endpoint must return valid JSON with `last_activity` in RFC3339 format
3. **Review logs**: Check the mloperator logs for culling-related messages
4. **Service must be running**: Culling only applies to services in the running state

See the [services timeout preset documentation](/docs/core/scheduling-presets/services-timeout/) for more examples and preset configurations.

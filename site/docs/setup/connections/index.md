---
title: "Connections"
title_link: "Connections"
is_index: true
sub_link: "connections"
meta_title: "Connections are how Polyaxon connects several types of external system and resources to your operations."
meta_description: "Connections are how Polyaxon connects several types of external system and resources to your operations."
tags:
  - agent
  - connections
  - specification
  - yaml
  - json
  - kubernetes
  - install
sidebar: "setup"
---

In order to reduce the amount of configurations in your Polyaxon's components and operations,
Polyaxon exposes a concept called Connections.

A connection is how you expose and connect your jobs to an artifacts store,
a volume, a git repo, a container registry, a slack channel, and other external systems.

Polyaxon is built on top of Kubernetes, so you can and in some cases will have to configure
access to some resources manually.
However for many use cases, for example, connecting to an S3 bucket,
using connections will reduce the amount of boilerplate in your jobs' specification files.

Every Polyaxon Agent deployment can configure:

 * `artifactsStore`
 * `connections`

All these configurations follow similar [specification](/docs/setup/connections/specification/).

> **Note**: the artifacts store definition will be added by default to the connections list.

## Example configuration

```yaml
artifactsStore:
  name: azure
  kind: wasb
  schema:
    bucket: "wasbs://test@container.blob.core.windows.net/"
  secret:
    name: "az-secret"
connections:
  - name: repo-test
    kind: git
    schema:
      url: https://gitlab.com/org/test
    secret:
      name: "gitlab-connection"
  - name: docker-connection
    description: "some description"
    kind: registry
    schema:
      url: org/repo
    secret:
      name: docker-conf
      mountPath: /kaniko/.docker
  - name: my-slack
    kind: slack
    secret:
      name: my-slack
```

## ArtifactsStore

Every time you deploy Polyaxon Community Edition platform or a Polyaxon Agent,
you will have to configure at least one connection, it's called the artifacts store.

This artifacts store is the default volume or blob storage that Polyaxon will use to save your runs' outputs and logs.

The `artifactsStore` must be of kind:
`host_path`, `volume_claim`, `gcs`, `s3`, or `wasb`.

For more details please check the [artifacts store section](/docs/setup/connections/artifacts/).

### Default behavior

When the user does not provide any `artifactsStore` configuration,
the default behavior is to use a local path on the host node for storing outputs and logs,
this behavior is oftentimes sufficient for users who are just trying the platform,
and don't want to deal with configuration steps.

## Connections

Polyaxon allows to configure multiple connections,
these connections can be multiple
[data volumes as well as cloud storages](/docs/setup/connections/artifacts/),
[git repos](/docs/setup/connections/git/),
[docker containers](/docs/setup/connections/registry/), database accesses, ...
this catalog of connections makes it very easy to organize access to several external systems and resources,
and there's no limitation on the number of connections you can define in this catalog.

You can define a custom catalog of connections per namespace if you want to isolate accessible resources by your users/teams,
or you can duplicate some or all connections in some namespaces and clusters.

For more details please check the [connection specification](/docs/setup/connections/specification/).

### Default behavior

By default, this catalog is empty and is not required for Polyaxon to function correctly.

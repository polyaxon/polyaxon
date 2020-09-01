---
title: "Connection Schemas"
sub_link: "connections/schemas"
meta_title: "Connections schemas in Polyaxon - Connections"
meta_description: " In order to leverage some built-in functionalities in Polyaxon, connections'
schema must follow a specification"
tags:
  - setup
  - polyaxon
  - connections
sidebar: "setup"
---

## Schema for volumes


### Example usage as init param

```yaml
params:
  data: {connection: "my-volume", init: true}
```

Specific files:

```yaml
params:
  data: {
    connection: "my-volume",
    init: true,
    artifacts: {'files': ['file1', 'path/to/file2']}
  }
```

### Example exposing the connection as an init container with custom container

```yaml
run:
  kind: service
  init: [{connection: "my-volume", container: {name: my-own-container, image: ...}}]
  container:
```

### Example exposing the connection inside the main container

```yaml
run:
  kind: service
  connections: ["my-volume"]
  container:
```

## Schema for host path


### Example definition

```yaml
name: my-volume
kind: host_path
schema:
  mountPath: "/tmp/outputs"
  hostPath: "/foo/bar"
```

### Example usage as init param

```yaml
params:
  data: {connection: "my-volume", init: true}
```

Specific files:

```yaml
params:
  data: {
    connection: "my-volume",
    init: true,
    artifacts: {'files': ['file1', 'path/to/file2']}
  }
```

### Example exposing the connection as an init container with custom container

```yaml
run:
  kind: service
  init: [{connection: "my-volume", container: {name: my-own-container, image: ...}}]
  container:
```

### Example exposing the connection inside the main container

```yaml
run:
  kind: service
  connections: ["my-volume"]
  container:
```

## Schema for S3/GCS/Azure Blob

### Fields

    * bucket: the bucket you want to expose in this connection.

### Example definition

```yaml
name: azure
kind: wasb
schema:
  bucket: "wasbs://logs@plxtest.blob.core.windows.net/"
 secret:
   name: "az-secret"
```

### Example usage as init param

```yaml
params:
  data:
    connection: "azure"
    init: true
```

Specific files:

```yaml
params:
  data:
    connection: "azure"
    init: true
    artifacts: {'files': ['file1', 'path/to/file2']}
```

### Example exposing the connection as an init container with custom container

```yaml
run:
  kind: service
  init:
    connection: "azure"
    container: {name: my-own-container, image: ...}}]
  container:
```

### Example exposing the connection inside the main container

```yaml
run:
  kind: service
  connections: ["azure"]
  container:
```

## Schema for git connections


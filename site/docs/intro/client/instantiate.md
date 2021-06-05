---
title: "How to instantiation the Python client"
sub_link: "client/instantiate"
meta_title: "A guide on how to instantiate the Python Client - Core Concepts"
meta_description: "Polyaxon's Python library tries to detect a context automatically, users can also change this behavior by providing auth, organization, project, and run references."
visibility: public
status: published
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

## Overview

When instantiating any of the Python clients or modules, Polyaxon performs a couple of checks to load a context if it exists. 
The context can be defined in the current user path if the CLI was initialized or authenticated, it can be defined using environment variables, 
or it can be defined by Polyaxon Scheduling if the module is called in an in-cluster job or service.  

## In-cluster

All Polyaxon clients and libraries will be configured automatically if used in-cluster.

e.g.

```python
run_client = RunClient()
```

Polyaxon provides a context for all its runs enabling users to access scoped tokens to communicate with the API.

## Locally with an authenticated Polyaxon CLI

If your Polyaxon CLI is authenticated, the Polyaxon client will be configured
automatically with the CLI authentication information.

e.g.

```python
run_client = RunClient()
```

The client will check for the currently authenticated user and raise if non found.

## Not in-cluster and no configured CLI

When you need to configure (and authenticate for Cloud and EE) a client in an environment outside of a Polyaxon cluster and no authenticated CLI, Polyaxon provides several options:

### Authentication with Environment variables:

You can set environment variables containing:

 * `POLYAXON_HOST`
 * `POLYAXON_AUTH_TOKEN`  (for EE and Cloud)

Once these environment variables are set, you can instantiate your client, e.g.

```python
run_client = RunClient()
```

Configuring and authenticating a client using environment variables could be useful to keep your code behave similarly in different environments.

### Provide a configured client:

```python
client = PolyaxonClient(token=API_TOKEN, config=ClientConfig(host=HOST, use_https=None, verify_ssl=None))
run_client = RunClient(owner="org1", project="project-name", run_uuid="uuid", client=client)
```

> **Note**: `API_TOKEN` is only required for EE and Cloud

## Changing the defined context

Since Polyaxon client and modules load any found context, it's sometimes useful to point the client to a different project or run other than the one cached locally or globally.
This is especially confusing when using Polyaxon Python client locally, the context will automatically load the current cached project and run, and several times users need to work on a specific entity.
In such cases instead of just instantiating a client or module with the default values, users should provide the entity they need to interact with.

Example changing project while defaulting to the same organization:

```python
run_client = RunClient(project="project-name")
```

Example providing the project and the organization, if the user has access to multiple organizations:

```python
run_client = RunClient(project="org-name/project-name")

# Or

run_client = RunClient(owner="org-name", project="project-name")
```

Example changing run while defaulting to the same project:

```python
run_client = RunClient(run_uuid="uuid")
```

> **Note**: If your script depends on a context and Polyaxon does not find any defined context it will raise an error.


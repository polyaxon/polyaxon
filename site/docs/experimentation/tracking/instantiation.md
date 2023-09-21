---
title: "How to instantiation the tracking module"
sub_link: "tracking/instantiation"
meta_title: "How to instantiate Polyaxon's tracking module - Tracking - Experimentation"
meta_description: "Polyaxon's Python library tries to detect a context automatically, users can also change this behavior by providing auth, organization, project, and run references."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
  - tracking
  - reference
  - sdk
sidebar: "experimentation"
---

## Overview

When instantiating any of the Python clients or modules, Polyaxon performs a couple of checks to load a context if it exists.
The context can be defined in the current user path if the CLI was initialized or authenticated, it can be defined using environment variables,
or it can be defined by Polyaxon Scheduling if the module is called in an in-cluster job or service.

## In-cluster

The tracking will be configured automatically if used in-cluster, e.g.

```python
from polyaxon import tracking

tracking.init()
```

Polyaxon provides a context for all its runs enabling users to access scoped tokens to communicate with the API.

## Locally with an authenticated Polyaxon CLI

If your Polyaxon CLI is authenticated, the Polyaxon client will be configured
automatically with the CLI authentication information, e.g.

 * If a run is locally cached it will be resumed otherwise a new one will be created

```python
from polyaxon import tracking

tracking.init()
```

 * To force the new behavior

```python
from polyaxon import tracking

tracking.init(is_new=True)
```

Please note that the client will check for the currently authenticated user and raise if non found.

## Not in-cluster and no configured CLI

When you need to configure (and authenticate for Cloud and EE) the tracking module in an environment outside of a Polyaxon cluster and no authenticated CLI, Polyaxon provides several options:

### Authentication with Environment variables:

You can set environment variables containing:

 * `POLYAXON_HOST`
 * `POLYAXON_AUTH_TOKEN`  (for EE and Cloud)

Once these environment variables are set, you can instantiate your client, e.g.

```python
from polyaxon import tracking

tracking.init()
```

Configuring and authenticating a client using environment variables could be useful to keep your code behave similarly in different environments.

### Provide a configured client:

```python
from polyaxon import tracking
from polyaxon.client import PolyaxonClient, RunClient

client = PolyaxonClient(token=API_TOKEN,
                        config=ClientConfig(host=HOST, use_https=None, verify_ssl=None))
run_client = RunClient(client=client)
tracking.init(client=run_client)
```

> **Note**: `API_TOKEN` is only required for EE and Cloud

## Changing the defined context

Since Polyaxon client and modules load any found context, it's sometimes useful to point the client to a different project or run other than the one cached locally or globally.
This is especially confusing when using Polyaxon Python client locally, the context will automatically load the current cached project and run, and several times users need to work on a specific entity.
In such cases instead of just instantiating a client or module with the default values, users should provide the entity they need to interact with.

Example changing project while defaulting to the same organization:

```python
from polyaxon import tracking

tracking.init(project="project-name")
```

Example providing the project and the organization, if the user has access to multiple organizations:

```python
from polyaxon import tracking

tracking.init(project="org-name/project-name")
# Or
tracking.init(owner="org-name", project="project-name")
```

Example changing the run while defaulting to the same project:

```python
from polyaxon import tracking

tracking.init(run_uuid="uuid")
```

> **Note**: If your script depends on a context and Polyaxon does not find any defined context it will raise an error.


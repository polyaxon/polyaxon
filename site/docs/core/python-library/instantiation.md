---
title: "How to instantiation the Python client"
sub_link: "python-library/instantiation"
meta_title: "How to instantiate Polyaxon's Python Client - Core Concepts"
meta_description: "Polyaxon's Python library tries to detect a context automatically, users can also change this behavior by providing auth, organization, project, and run references."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
sidebar: "core"
---

## Overview

When instantiating any of the Python clients or modules, Polyaxon performs a couple of checks to load a context if it exists.
The context can be defined in the current user path if the CLI was initialized or authenticated, it can be defined using environment variables,
or it can be defined by Polyaxon Scheduling if the module is called in an in-cluster job or service.

## In-cluster

All Polyaxon clients and libraries will be configured automatically if used in-cluster, e.g.

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient()
run_client = RunClient()
```

Polyaxon provides a context for all its runs enabling users to access scoped tokens to communicate with the API.
Additionally, the client will automatically resolve the currently running operation and the project it belongs to.

## Locally with an authenticated Polyaxon CLI

If your Polyaxon CLI is authenticated, the Polyaxon client will be configured
automatically with the CLI authentication information, e.g.

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient()
run_client = RunClient()
```

The client will check for the currently authenticated user and raise if non found.

Please note the client will automatically detect the [local cache](/docs/core/cli/cache/) and will use the cached project and run.

If you have local cache and you need to use a different project ro run, similar to switching CLI context, users need to pass the full porject or run context, i.e.:

```python
from polyaxon.client import ProjectClient, RunClient

# For projects
project_client = ProjectClient(project="OWNER/PROJECT")
# Or
project_client = ProjectClient(owner="OWNER", project="PROJECT")
# For runs
run_client = RunClient(project="OWNER/PROJECT", run_uuid="UUID")
# Or
run_client = RunClient(owner="OWNER", project="PROJECT", run_uuid="UUID")
```

## Not in-cluster and no configured CLI

When you need to configure (and authenticate for Cloud and EE) a client in an environment outside of a Polyaxon cluster and no authenticated CLI, Polyaxon provides several options:

### Authentication with Environment variables:

You can set environment variables containing:

 * `POLYAXON_HOST`
 * `POLYAXON_AUTH_TOKEN`  (for EE and Cloud)

Once these environment variables are set, you can instantiate your client, e.g.

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient()
run_client = RunClient()
```

Configuring and authenticating a client using environment variables could be useful to keep your code behave similarly in different environments.

### Provide a configured client:

```python
from polyaxon.client import PolyaxonClient, ProjectClient, RunClient

client = PolyaxonClient(token=API_TOKEN,
                        config=ClientConfig(host=HOST, use_https=None, verify_ssl=None))

project_client = ProjectClient(owner="org1", project="project-name", client=client)
run_client = RunClient(owner="org1", project="project-name", run_uuid="uuid", client=client)
```

> **Note**: `API_TOKEN` is only required for EE and Cloud

## Changing the defined context

Since Polyaxon client and modules load any found context, it's sometimes useful to point the client to a different project or run other than the one cached locally or globally.
This is especially confusing when using Polyaxon Python client locally, the context will automatically load the current cached project and run, and several times users need to work on a specific entity.
In such cases instead of just instantiating a client or module with the default values, users should provide the entity they need to interact with.

Example changing project while defaulting to the same organization:

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient(project="project-name")
run_client = RunClient(project="project-name")
```

Example providing the project and the organization, if the user has access to multiple organizations:

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient(project="org-name/project-name")
run_client = RunClient(project="org-name/project-name")

# Or
project_client = ProjectClient(owner="org-name", project="project-name")
run_client = RunClient(owner="org-name", project="project-name")
```

Example changing the run while defaulting to the same project:

```python
from polyaxon.client import ProjectClient, RunClient

project_client = ProjectClient()
run_client = RunClient(run_uuid="uuid")
```

> **Note**: If your script depends on a context and Polyaxon does not find any defined context it will raise an error.

## Configuration using environment variable

You can configure the client directly via environment variables, Polyaxon provides several options, the main ones are:

```bash
export POLYAXON_HOST ...
export POLYAXON_VERIFY_SSL ...
export POLYAXON_SSL_CA_CERT ...
export POLYAXON_CERT_FILE ...
export POLYAXON_KEY_FILE ...
export POLYAXON_DEBUG ...
export POLYAXON_TIMEOUT ...
export POLYAXON_LOG_LEVEL ...
```

> **Note**: If you are running a script in cluster, Polyaxon takes care of exposing these environment variables.

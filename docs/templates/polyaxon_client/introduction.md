Polyaxon client is python module that includes several clients that can be used to interact
with Polyaxon API in a programmatic way.

## Install

```bash
$ pip install -U polyaxon-client
```

for python3

```bash
$ pip3 install -U polyaxon-client
```

## Clients

This module includes several clients that can be used to interact
with Polyaxon API in a programmatic way.

 * [Auth](clients/auth): A client for handling authentication and user information.
 * [Cluster](clients/cluster): A client for getting cluster and cluster nodes information.
 * [User](clients/user): A client to manage users and superuser roles.
 * [Project](clients/project): A client for doing CRUD operations on projects, as well as getting and creating experiments and experiment groups, creating and stopping tensorboard/notebook, and uploading code.
 * [Experiment group](clients/experiment_group): A client for doing CRUD operations on experiment groups, as well as fetching experiments per group.
 * [Experiment](clients/experiment): A client for doing CRUD operations on experiments, as well as statuses, jobs, resources, and logs.
 * [Experiment Job](clients/experiment_job): A client for getting information, resources, and logs of experiment jobs.
 * [Job](clients/job): A client for getting information, resources, and logs of jobs.
 * [Build Job](clients/build_job): A client for getting information, resources, and logs of build jobs.
 * [Version](clients/version): A client to get current and supported versions of several Polyaxon component.


## Usage

```python
from polyaxon_client.clients import PolyaxonClients

polyaxon_clients = PolyaxonClients(
    host=POLYAXON_IP,
    token=MY_TOKEN, http_port=POLYAXON_HTTP_PORT,
    ws_port=POLYAXON_WS_PORT)

polyaxon_clients.auth
polyaxon_clients.cluster
polyaxon_clients.user
polyaxon_clients.project
polyaxon_clients.experiment
polyaxon_clients.experiment_group
polyaxon_clients.experiment_job
polyaxon_clients.job
polyaxon_clients.build_job
polyaxon_clients.version
```

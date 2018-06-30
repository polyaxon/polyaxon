[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.org/polyaxon/polyaxon-client.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-client)
[![PyPI version](https://badge.fury.io/py/polyaxon-client.svg)](https://badge.fury.io/py/polyaxon-client)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-client

Python clients to interact with Polyaxon API.


## Install

```bash
$ pip install -U polyaxon-client
```

## Clients

This module includes several clients that can be used to interact
with Polyaxon API in a programmatic way.

 * [Auth](https://docs.polyaxon.com/polyaxon_client/auth): A client for handling authentication and user information.
 * [Cluster](https://docs.polyaxon.com/polyaxon_client/cluster): A client for getting cluster and cluster nodes information.
 * [User](https://docs.polyaxon.com/polyaxon_client/user): A client to manage users and superuser roles.
 * [Project](https://docs.polyaxon.com/polyaxon_client/project): A client for doing CRUD operations on projects, as well as getting and creating experiments and experiment groups, creating and stopping tensorboard/notebook, and uploading code.
 * [Experiment](https://docs.polyaxon.com/polyaxon_client/experiment): A client for doing CRUD operations on experiments, as well as statuses, jobs, resources, and logs.
 * [Experiment group](https://docs.polyaxon.com/polyaxon_client/experiment_group): A client for doing CRUD operations on experiment groups, as well as fetching experiments per group.
 * [Experiment Job](https://docs.polyaxon.com/polyaxon_client/experiment_job): A client for getting information, resources, and logs of experiment jobs.
 * [Job](https://docs.polyaxon.com/polyaxon_client/job): A client for getting information, resources, and logs of jobs.
 * [Build Job](https://docs.polyaxon.com/polyaxon_client/build_job): A client for getting information, resources, and logs of build jobs.
 * [Version](https://docs.polyaxon.com/polyaxon_client/version): A client to get current and supported versions of several Polyaxon component.


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


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client?ref=badge_large)

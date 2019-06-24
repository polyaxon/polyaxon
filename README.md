[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.org/polyaxon/polyaxon-client.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-client)
[![PyPI version](https://badge.fury.io/py/polyaxon-client.svg)](https://badge.fury.io/py/polyaxon-client)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a33947d729f94f5da7f7390dfeef7f94)](https://www.codacy.com/app/polyaxon/polyaxon-client?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/polyaxon-client&amp;utm_campaign=Badge_Grade)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-client

Python clients to interact with Polyaxon API.


## Install

```bash
$ pip install -U polyaxon-client
```

## Clients

This module includes a client that can be used to interact
with Polyaxon API in a programmatic way.

 * [Auth](https://docs.polyaxon.com/references/polyaxon-client-python/auth): A client for handling authentication and user information.
 * [Cluster](https://docs.polyaxon.com/references/polyaxon-client-python/cluster): A client for getting cluster and cluster nodes information.
 * [User](https://docs.polyaxon.com/references/polyaxon-client-python/user): A client to manage users and superuser roles.
 * [Project](https://docs.polyaxon.com/references/polyaxon-client-python/project): A client for doing CRUD operations on projects, as well as getting and creating experiments and experiment groups, creating and stopping tensorboard/notebook, and uploading code.
 * [Experiment](https://docs.polyaxon.com/references/polyaxon-client-python/experiment): A client for doing CRUD operations on experiments, as well as statuses, jobs, resources, and logs.
 * [Experiment group](https://docs.polyaxon.com/references/polyaxon-client-python/experiment-group): A client for doing CRUD operations on experiment groups, as well as fetching experiments per group.
 * [Experiment Job](https://docs.polyaxon.com/references/polyaxon-client-python/experiment-job): A client for getting information, resources, and logs of experiment jobs.
 * [Job](https://docs.polyaxon.com/references/polyaxon-client-python/job): A client for getting information, resources, and logs of jobs.
 * [Build Job](https://docs.polyaxon.com/references/polyaxon-client-python/build-job): A client for getting information, resources, and logs of build jobs.
 * [Bookmark](https://docs.polyaxon.com/references/polyaxon-client-python/bookmark): A client for getting bookmarks.
 * [Version](https://docs.polyaxon.com/references/polyaxon-client-python/version): A client to get current and supported versions of several Polyaxon component.


## Usage

```python
from polyaxon_client import PolyaxonClient

polyaxon_client = PolyaxonClient(
    host=POLYAXON_IP,
    token=MY_TOKEN, http_port=POLYAXON_HTTP_PORT,
    ws_port=POLYAXON_WS_PORT)

polyaxon_client.auth
polyaxon_client.cluster
polyaxon_client.user
polyaxon_client.project
polyaxon_client.experiment
polyaxon_client.experiment_group
polyaxon_client.experiment_job
polyaxon_client.job
polyaxon_client.build_job
polyaxon_client.bookmark
polyaxon_client.version
```

e.g. list projects for a user

```python
polyaxon_client.project.list_projects(username, page=1)
```

e.g. list experiments for a project

```python
polyaxon_client.project.list_experiments(
    username,
    project_name,
    independent=None,
    group=None,
    metrics=None,
    params=None,
    query=None,
    sort=None,
    page=1)
```


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/setup/)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/concepts/quick-start/) to start training your first experiment.


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client?ref=badge_large)

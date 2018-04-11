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

 * `Auth`: A client for handling authentication and user information.
 * `Cluster`: A client for getting cluster and cluster nodes information.
 * `Data`: A client for getting data.
 * `Experiment`: A client for doing CRUD operations on experiments, as well as statuses, jobs, resources, and logs.
 * `Experiment group`: A client for doing CRUD operations on experiment groups, as well as fetching experiments per group.
 * `Job`: A client for getting information, resources, and logs of jobs.
 * `Project`: A client for doing CRUD operations on projects, as well as getting and creating experiments and experiment groups, creating and stopping tensorboard/notebook, and uploading code.
 * `User`: A client to manage users and superuser roles.
 * `Version`: A client to get current and supported versions of several Polyaxon component.


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-client?ref=badge_large)

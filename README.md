[![Build Status](https://travis-ci.org/polyaxon/polyaxon-client.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-client)
[![PyPI version](https://badge.fury.io/py/polyaxon-client.svg)](https://badge.fury.io/py/polyaxon-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg)](https://gitter.im/polyaxon/polyaxon)


# polyaxon-client

Python clients to interact with Polyaxon API.


## Install

```bash
$ pip install -U polyaxon-client
```

## Clients

This module includes several clients that can be used to interact
with Polyaxon API in a programmatic way.

 * `Auth`: A client for handling logging and user information.
 * `Cluster`: A client for getting cluster and cluster nodes information.
 * `Data`: A client to getting data.
 * `Experiment`: A client for doing CRUD operations on experiments, as well as statuses, jobs, resources, and logs.
 * `Experiment `group: A client for doing CRUD operations on experiment groups, as well as fetching experiments per group.
 * `Job`: A client for getting information, resources, and logs of jobs.
 * `Project`: A client for doing CRUD operations on project, as well as getting and creating experiments and experiment groups, creating and stopping tensorboard, and uploading code.
 * `User`: A client to manage users and superuser roles.
 * `Version`: A client to get current and supported versions of several Polyaxon component.


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.


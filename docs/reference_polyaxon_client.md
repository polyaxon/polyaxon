Polyaxon client is python module that includes several clients that can be used to interact
with Polyaxon API in a programmatic way.

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

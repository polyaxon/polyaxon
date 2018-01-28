Polyaxon CLI is a tool and a client to interact with Polyaxon,
it allows you to manage your cluster, users, projects, and experiments.

## Installation

To install Polyaxon CLI please refer to the [installation documentation](/installation/install_polyaxon_cli).


## Help

To get help from The Polyaxon CLI, you can run the following

```bash
$ polyaxon --help
```

To get help for any Polyaxon CLI Command, you can run the following

```bash
$ polyaxon command --help
```

## Commands References

 * [Auth](commands/auth)
 * [Check](commands/check)
 * [Config](commands/config)
 * [Init](commands/init)
 * [Project](commands/project)
 * [Upload](commands/upload)
 * [Run](commands/run)
 * [Experiment Group](commands/experiment_group)
 * [Experiment](commands/experiment)
 * [Job](commands/job)
 * [Cluster](commands/cluster)
 * [Version](commands/version)

## Caching

When using the Polyaxon CLI to run a command requiring a project, group, experiment, and/or a job,
you can always specify the values for these options, example:

 * `$ polyaxon project --project=user_1/project_10 get`
 * `$ polyaxon experiment --project=user_1/project_10 --experiment=2 get`
 * `$ polyaxon group --project=user_1/project_10 --group=2 experiments`
 * `$ polyaxon job --project=user_1/project_10 --experiment=3 --job=2 logs`


Polyaxon CLI allows also you to omit these options, i.e. project, experiment group, experiment, and job, the CLI does the following:

 1. When a username is missing, the username of the logged-in user is used.
 2. When a project name is missing, the name of the currently initialized project is used.
 3. When an experiment group, experiment, or job is missing, the last value is used.
 4. If no values are found, the CLI will show an error.

Same commands with caching:

 * `$ polyaxon project get`
 * `$ polyaxon experiment get`
 * `$ polyaxon group experiments`
 * `$ polyaxon job logs`

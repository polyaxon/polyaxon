Polyaxon CLI is a tool and a client to interact with your Polyaxon,
it allows you to manage you cluster, users, projects, and experiments.

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


## Caching

When using the Polyaxon CLI to run command requiring a project,
you can always specify the options for project, experiment group, experiment, job, example:

 * `$ polyaxon project get user_1/project_10`
 * `$ polyaxon experiment get 2 --project=user_1/project_10`
 * `$ polyaxon group experiments 3 --project=user_1/project_10`
 * `$ polyaxon job logs 50c62372137940ca8c456d8596946dd7 --project=user_1/project_10 --experiment=3`


Polyaxon CLI allows you to omit these options, i.e. project, experiment group, experiment, and job, the CLI does the following:

 1. When a username is missing, the username of the logged-in user is used.
 2. When a project name is missing, the name of the currently initialized project is used.
 3. When an experiment group, experiment, or job is missing, the last value is used.

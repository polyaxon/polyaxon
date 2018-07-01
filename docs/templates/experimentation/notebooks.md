Polyaxon allows users to run notebook jobs on project level, these jobs are subject to the same permissions of the project they belong to.

[Notebooks](https://jupyter.org/) allow users to create and share documents that contain live code,
visualizations and explanatory texts.

Notebooks are great for interactively writing and debugging your code and visualizing your results and data.

## Start a notebook

We assume that you have already a [project](projects) created and initialized, and code uploaded.

Starting notebook is similar to running any other Polyaxon job, i.e. you need to define polyaxonfile containing:

 * [version](/polyaxonfile_specification/sections#version)
 * [kind](/polyaxonfile_specification/sections#kind): in this case this value should be `plugin`.
 * [project](/polyaxonfile_specification/sections#project)
 * [run](/polyaxonfile_specification/sections#version)

Let's create a simple polyaxonfile_notebook.yml

```yaml
---
version: 1

kind: notebook

build:
  image: python:3
  build_steps:
    - pip3 install jupyter
```

Now we can start the jupyter notebook on the project

```bash
$ polyaxon notebook -f polyaxonfile_notebook.yml

Notebook is being deployed for project `mnist`

It may take some time before you can access the dashboard.

Your notebook will be available on:

    http://192.168.64.6:30087/notebook/admin/mnist/
```

Polyaxon will create a docker image based on the specification in the polyaxonfile and
start a jupyter notebook with the same permissions of the project.
This means that if the project is private the notebook will only be visible to the project owner and superusers.

!!! tip
    You can also execute `notebook start` with `-u` option, to upload before resuming the start the command,
    In that case `polyaxon upload is not necessary`

    ```bash
    $ polyaxon notebook -f polyaxonfile_notebook.yml -u
    ```


Since the notebook is create with polyaxonfile, it can be customized in the same way as any other job, e.g. you can customize the resources, request GPUs ...

```yaml
---
version: 1

kind: notebook

environment:
  resources:
    cpu:
      requests: 2
      limits: 4
    gpu:
      requests: 1
      limits: 1
    memory:
      requests: 512
      limits: 2048

build:
  image: python:3
  build_steps:
    - pip3 install jupyter
```

## Stop a notebook

To stop a notebook, run the following command in your terminal

```bash
$ polyaxon notebook stop
```


!!! info "More details"
    For more details about this command please run `polyaxon notebook --help`,
    or check the [command reference](/polyaxon_cli/commands/notebook)

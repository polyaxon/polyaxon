---
title: "JupyterLab"
meta_title: "JupyterLab"
meta_description: "Polyaxon makes it easy to start JupyterLab on your projects for you and your team members."
custom_excerpt: "JupyterLab is an extensible environment for interactive and reproducible computing, based on the Jupyter Notebook and Architecture."
image: "../../content/images/integrations/jupyter-lab.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - scheduling
  - experimentation
featured: false
visibility: public
status: beta
---

## Overview
 
Polyaxon makes it easy to start Jupyter Lab on your projects for you and your team members. users acn run Jupyter Lab jobs on projects level, 
these jobs are subject to the same permissions of the project they belong to.

Jupyter Lab is an alternative backend when creating notebooks on Polyaxon.

> To learn more about polyaxon notebook CLI, run `polyaxon notebook --help`, or check the [command reference](references/polyaxon-cli/notebook/)

> Future releases will allow you to specify a default notebook image and backend to start notebooks/labs without providing a polyaxonfile

## Create a polyaxonfile for your Jupyter Lab

To create a Jupyter Lab, you need a polyaxonfile to customize the container running your notebook:

```yaml
version: 1

kind: notebook

environment:
  backend: lab

build:
  image: python:3
  build_steps:
    - pip3 install jupyterlab==0.33.12
```

## Start the Jupyter Lab

Now you can start the Jupyter Lab on the project

```bash
polyaxon notebook start -f polyaxonfile_notebook.yml


Notebook is being deployed for project `mnist`

It may take some time before you can access the dashboard.

Your notebook will be available on:

    http://192.168.64.6:30087/notebook/admin/mnist/
```

Notebook commands accept [context switching])(/references/polyaxon-cli/#switching-context) which means that you can create a Jupyter Lab for project other than the one initialized, 
or without initializing a local folder.

 
```bash
polyaxon notebook start -p my-project-name -f polyaxonfile_notebook.yml
```

## Stop a running notebook

To stop a Jupyter Lab, run the following command in your terminal

```bash
polyaxon notebook stop
```

or

```bash
polyaxon notebook -p my-project-name stop
```

## More info about how to customize notebooks

Learn more about the notebook concept in [Polyaxon](/concepts/notebooks/), and how you can customize notebooks [run environment](/references/polyaxonfile-yaml-specification/#notebook-sections) 

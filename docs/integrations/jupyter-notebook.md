---
title: "Jupyter Notebook"
meta_title: "Jupyter Notebook"
meta_description: "Polyaxon makes it easy to start Jupyter Notebooks on your projects for you and your team members."
custom_excerpt: "The Jupyter Notebook is an incredibly powerful tool for interactively developing and presenting data science projects. A notebook integrates code and its output into a single document that combines visualisations, narrative text, mathematical equations, and other rich media."
image: "../../content/images/integrations/jupyter-notebook.png"
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
status: published
---

## Overview
 
Polyaxon makes it easy to start Jupyter Notebooks on your projects for you and your team members. users acn run notebook jobs on projects level, 
these jobs are subject to the same permissions of the project they belong to.

> To learn more about polyaxon notebook CLI, run `polyaxon notebook --help`, or check the [command reference](references/polyaxon-cli/notebook/)

> Future releases will allow you to specify a default notebook image and backend to start notebooks/labs without providing a polyaxonfile

## Create a polyaxonfile for your notebook

To create a notebook, you need a polyaxonfile to customize the container running your notebook:

```yaml
version: 1

kind: notebook

build:
  image: python:3
  build_steps:
    - pip3 install jupyter
```

## Start the notebook

Now you can start the jupyter notebook on the project

```bash
polyaxon notebook start -f polyaxonfile_notebook.yml


Notebook is being deployed for project `mnist`

It may take some time before you can access the dashboard.

Your notebook will be available on:

    http://192.168.64.6:30087/notebook/admin/mnist/
```

Notebook commands accept [context switching])(/references/polyaxon-cli/#switching-context) which means that you can create a notebook for project other than the one initialized, 
or without initializing a local folder.

 
```bash
polyaxon notebook start -p my-project-name -f polyaxonfile_notebook.yml
```

## Stop a running notebook

To stop a notebook, run the following command in your terminal

```bash
polyaxon notebook stop
```

or

```bash
polyaxon notebook -p my-project-name stop
```

## More info about how to customize notebooks

Learn more about the notebook concept in [Polyaxon](/concepts/notebooks/), and how you can customize notebooks [run environment](/references/polyaxonfile-yaml-specification/#notebook-sections) 

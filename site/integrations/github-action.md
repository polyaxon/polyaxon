---
title: "Github Action"
meta_title: "Github Action"
meta_description: "Polyaxon can be used with GitHub Actions to create a continuous machine learning pipeline and CI/CD for Machine Learning Projects."
custom_excerpt: "GitHub Actions makes it easy to automate all your software workflows, now with world-class CI/CD. Build, test, and deploy your code right from GitHub. Make code reviews, branch management, and issue triaging work the way you want."
image: "../../content/images/integrations/github.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - pipelines
  - scheduling
  - dags
  - automation
featured: false
popularity: 0
visibility: public
status: published
---

You can use Polyaxon CLI in your Github Actions to lint and check your Polyaxonfiles, pull information about projects and runs, and submit operations remotely from Github.

## Lint & Check

In order to automate the process of checking and linting your Polyaxonfile, you can use `polyaxon/polyaxon-cli`
docker image in your Github Actions similarly to how you would do in your local machine:

```yaml
name: Test Component

on: [push]

jobs:
  check:
    runs-on: ubuntu-latest
    container: docker://polyaxon/polyaxon-cli:1.x.x.
    steps:
      - uses: actions/checkout@v4
      - name: lint
        run: |
          polyaxon check -f polyaxonfies/operation.yaml
          polyaxon check -f polyaxonfies/component.yaml --lint
      - name: validate
        run: polyaxon check -f polyaxonfies/component.yaml -P activation=relu -P lr=0.01
```

## Submit runs

In order to submit runs from a Github action, you need to provide information about your `host` if you are using Polyaxon CE,
and your token if you are using one of Polyaxon commercial products.

This example assumes that the user changes the `operation.yaml` file with new params and/or new information about the environment (e.g. GPU) on every push.

```yaml
name: Submit Job

on: [push]

jobs:
  check:
    runs-on: ubuntu-latest
    container: docker://polyaxon/polyaxon-cli:1.x.x.
    steps:
      - uses: actions/checkout@v4
      - name: config
        run: polyaxon config --host=${{ secrets.POLYAXON_HOST }}
      - name: login
        run: polyaxon login -t ${{ secrets.POLYAXON_TOKEN }}
      - name: submit
        run: polyaxon run -p MY-PROJECT -f operation.yaml
```


> **Note**: You can expose `POLYAXON_TOKEN`, `POLYAXON_HOST`, and other configurations as env vars, in that case `polyaxon config` and `polyaxon login` commands are not required.

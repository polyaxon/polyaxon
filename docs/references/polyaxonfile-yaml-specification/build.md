---
title: "Build - Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification/build"
meta_title: "Build Section - Polyaxonfile YAML Specification Sections - Polyaxon References"
meta_description: "Build Section - Polyaxonfile YAML Specification Sections."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

## Overview

This is where you define how you build an image to run your code.
This section defines the following values/subsections:

 * image [required if dockerfile not provided]: the base image polyaxon will use to build an image for you to run your code.
 * dockerfile [required if image note provided]: the path to the dockerfile in your code repo.
 * context[optional]: path to the context to mount and look for any file used for the build process.
 * build_steps [optional]: steps are basically a list of ops that Polyaxon use with docker
 `RUN` to install/run further operations you define in the list.
 * env_vars [optional]: environment variables are also a list of tuples of 2 elements, that polyaxon will use to add env variables in the docker image.
 * commit [optional]: the commit to use for creating the build.
 * branch [optional]: the branch to use for creating the build.
 * nocache [optional]: to force rebuild the image. 

## Example using commit

```yaml
build:
  image: my_image
  build_steps:
    - pip install PILLOW
    - pip install scikit-learn
  env_vars:
    - [KEY1, VALUE1]
    - [KEY2, VALUE2]
```

## Example using commit

```yaml
build:
  image: my_image
  build_steps:
    - pip install PILLOW
    - pip install scikit-learn
  env_vars:
    - [KEY1, VALUE1]
    - [KEY2, VALUE2]
  commit: 14e9d652151eb058afa0b51ba110671f2ca10cbf
```

## Example using branch name

```yaml
build:
  image: ubuntu
  branch: branch_dev
```

## Example using a Dockerfile


```yaml
build:
  dockefile: path/to/Dockerfile
  commit: 14e9d652151eb058afa0b51ba110671f2ca10cbf
```

## Example using an image and a context


```yaml
build:
  image: my_image
  context: path/to/context
  build_steps:
    - pip install PILLOW
    - pip install scikit-learn
  env_vars:
    - [KEY1, VALUE1]
    - [KEY2, VALUE2]
  commit: 14e9d652151eb058afa0b51ba110671f2ca10cbf
```

## Example using a Dockerfile and a context


```yaml
build:
  dockefile: path/to/Dockerfile
  context: different/path/to/context
```

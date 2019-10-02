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

 * image [required if dockerfile not provided]: the base image Polyaxon will use to build an image for you to run your code.
 * dockerfile [required if image not provided]: the path to the dockerfile in your code repo.
 * context[optional]: path to the context to mount and look for any file used for the build process.
 * build_steps [optional]: steps are basically a list of ops that Polyaxon use with docker
 `RUN` to install/run further operations you define in the list.
 * env_vars [optional]: environment variables are also a list of tuples of 2 elements, that Polyaxon will use to add env variables in the docker image.
 * lang_env [optional]: an easy way to expose language environment on your dockerfile.
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
  dockerfile: path/to/Dockerfile
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
  dockerfile: path/to/Dockerfile
  context: different/path/to/context
```

## Example using an environment with resources

```yaml
build:
  environment:
    resources:
      cpu:
        requests: 1
        limits: 2
  dockerfile: path/to/Dockerfile
  context: different/path/to/context
```

## Exposing language environment

```yaml
build:
  ...
  lang_env: 'C.UTF-8'
```

Will result in these env section added to your dockerfile

```
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV LANGUAGE C.UTF-8
```

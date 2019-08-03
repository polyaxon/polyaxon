[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.com/polyaxon/polyaxon-dockerizer.svg?branch=master)](https://travis-ci.com/polyaxon/polyaxon-dockerizer)
[![PyPI version](https://badge.fury.io/py/polyaxon-dockerizer.svg)](https://badge.fury.io/py/polyaxon-dockerizer)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a33947d729f94f5da7f7390dfeef7f94)](https://www.codacy.com/app/polyaxon/polyaxon-dockerizer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/polyaxon-dockerizer&amp;utm_campaign=Badge_Grade)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-dockerizer

Python tool to generate dockerfiles compatible with Polyaxon dockerizer and Polyaxon CLI local run.


## Install

```bash
$ pip install -U polyaxon-dockerizer
```

## Usage

### Generate Dockerfiles

```python
from polyaxon_dockerizer import generate
         
generate(repo_path,
         from_image,
         build_steps=['apt-get install git', 'pip install tensorflow'],
         env_vars=[['ENV_VAR1', 'VALUE1'], ['ENV_VAR2', 'VALUE2']],
         nvidia_bin=None,
         lang_env='en_US.UTF-8',
         uid=2222,
         gid=2222)
```

### Build images

```python
from polyaxon_dockerizer import build

build(build_context,
      image_tag,
      image_name,
      nocache,
      credstore_env=None,
      registries=None)
```


### Build & Push images

```python
from polyaxon_dockerizer import build_and_push

build_and_push(build_context,
               image_tag,
               image_name,
               nocache,
               credstore_env=None,
               registries=None)
```


## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/setup/)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/concepts/quick-start/) to start training your first experiment.

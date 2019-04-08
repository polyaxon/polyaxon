[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.org/polyaxon/polyaxon-dockgen.svg?branch=master)](https://travis-ci.org/polyaxon/polyaxon-dockgen)
[![PyPI version](https://badge.fury.io/py/polyaxon-dockgen.svg)](https://badge.fury.io/py/polyaxon-dockgen)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a33947d729f94f5da7f7390dfeef7f94)](https://www.codacy.com/app/polyaxon/polyaxon-dockgen?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/polyaxon-dockgen&amp;utm_campaign=Badge_Grade)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-dockgen

Python tool to generate dockerfiles compatible with Polyaxon dockerizer and Polyaxon CLI local run.


## Install

```bash
$ pip install -U polyaxon-dockgen
```

## Usage

```python
from polyaxon_dockgen import generate

generate(repo_path,
         from_image,
         build_steps=None,
         env_vars=None,
         nvidia_bin=None,
         set_lang_env=True)
```

## Install polyaxon

Please check [polyaxon installation guide](https://docs.polyaxon.com/installation/introduction)


## Quick start

Please check our [quick start guide](https://docs.polyaxon.com/quick_start) to start training your first experiment.


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-dockgen.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Fpolyaxon-dockgen?ref=badge_large)

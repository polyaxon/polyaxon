[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://travis-ci.com/polyaxon/ocular.svg?branch=master)](https://travis-ci.com/polyaxon/ocular)
[![PyPI version](https://badge.fury.io/py/ocular.svg)](https://badge.fury.io/py/ocular)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a33947d729f94f5da7f7390dfeef7f94)](https://www.codacy.com/app/polyaxon/ocular?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/ocular&amp;utm_campaign=Badge_Grade)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# ocular
A tool for observing Kubernetes pods' statuses in real time.

## Description

Often times it's very hard to translate a Kubernetes event to a concrete state, 
and that's the gap that ocular tries fill, i.e. return one of the following statuses:

```
created
building
unschedulable
scheduled
running
succeeded
failed
stopped
unknown
``` 

ocular returns as well a condensed information about the reason of that status.

## Install

```bash
$ pip install -U ocular
```

## Usage

```python
import ocular
from kubernetes import client

api_client = client.api_client.ApiClient(configuration=...)

for pod_state in ocular.monitor(api_client, 
                                namespace='polyaxon', 
                                container_names=('polyaxon-experiment-job',), 
                                label_selector='app in (workers,dashboard),type=runner'):
    print(pod_state)
```

Results

```
...
>> {'status': 'unknown', 'message': 'Unknown pod conditions', 'details': {'event_type': 'ADDED', 'labels': ...
>> {'status': 'building', 'message': None, 'details': {'event_type': 'MODIFIED', 'labels': ...
>> {'status': 'building', 'message': 'PodInitializing', 'details': {'event_type': 'MODIFIED', 'labels': ...
>> {'status': 'building', 'message': 'PodInitializing', 'details': {'event_type': 'MODIFIED', 'labels': ...
>> {'status': 'running', 'message': None, 'details': {'event_type': 'MODIFIED', 'labels': ...
>> {'status': 'running', 'message': None, 'details': {'event_type': 'MODIFIED', 'labels': ...
>> {'status': 'succeeded', 'message': None, 'details': {'event_type': 'MODIFIED', 'labels': ...
...
```


## License

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fpolyaxon%2Focular.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fpolyaxon%2Focular?ref=badge_large)

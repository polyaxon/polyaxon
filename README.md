[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-0.3.8-brightgreen.svg?style=flat)](https://docs.polyaxon.com)
![Release](https://img.shields.io/badge/release-0.3.8-brightgreen.svg?longCache=true)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-examples

Code for polyaxon tutorials and examples.

This repository contains examples of using Polyaxon with all major Machine Learning and Deep Learning libraries, 
including fastai, torch, sklearn, chainer, caffe, keras, tensorflow, mxnet, and Jupyter notebooks.

If you don't see something you need, Don't hesitate to contact us.

## Examples Structure

This repository has 2 main directories containing examples for running experiments in-cluster, i.e. scheduled and managed by a Polyaxon Deployment, 
as well as experiment running on different platforms and tracked by Polyaxon, i.e. experiments running on laptops, spark, other platforms.

The examples have a comment `# Polyaxon` to show what is added to a raw code to enable the lightweight Polyaxon integration.

### Getting Started

If you are new to Polyaxon we recommend reading our [quick-start](https://docs.polyaxon.com/quick_start/) guide which explains some of the core Platform capabilities.

### Setup & Installation

Please check our [documentation](https://docs.polyaxon.com) to learn about how to deploy Polyaxon.

All examples (in-cluster and on other examples running on other platforms) require our [client](https://github.com/polyaxon/polyaxon-client) to track and add instrumentation to the experiments.
 
### in-cluster Examples

In order to run these examples, you need to deploy a Polyaxon with a scheduling component enabled.

### Tracking Examples

These examples should run with all type of Polyaxon deployments.

To run the tracking examples, you need to configure a client to communicate with Polyaxon API, 
there are many ways to configure the client, in this example we use an environment approach to have minimal impact on the code, 
in other terms, this approach allow us to create an experiment with the minimum code required:

```python
from polyaxon_client.tracking import Experiment

...
experiment = Experiment(project='project-name')
experiment.create()
...
# Tracking here, e.g.

experiment.log_params(loss=args.loss, penalty=args.penalty, l1_ratio=args.l1_ratio, max_iter=args.max_iter, tol=args.tol)
...
experiment.log_data_ref(data=X, data_name='dataset_X')
...
experiment.log_metrics(loss=0.1, accuracy=0.9)
```

If you wish to explicitly set the configuration for your experiment, you need to provide a configured client:

```python
client = PolyaxonClient(host='123.123.123.123', token='my-token-hash')  # See other params, i.e. http_port, ws_port, ...
experiment = Experiment(project='project-name', client=client)

# The rest is the same
...
``` 

To learn more how to configure Polyaxon Client & Polyaxon Tracking, please see our [documentation](https://docs.polyaxon.com)

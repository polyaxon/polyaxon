## What libraries and frameworks does Polyaxon support

Polyaxon supports all popular deep learning frameworks and machine learning libraries.

## I deployed a Kubernetes cluster using kubeadm and Polyaxon does not seem to work

Please check that networking is working as intended.
Some users reported that deploying Kubernetes with Canal for networking works better.

## Is Polyaxon useful only for teams

The target audience of Polyaxon, are individuals or teams looking for more organized and rigorous workflow,
with immutable and reproducible experiments, and an organized and easy way to access logs and outputs.

## Does Polyaxon support serving models

Currently, Polyaxon does not provide an in-cluster mechanism for deploying models.
Polyaxon tries to solve problems related to experimentation.

We provide easy ways to test your models, and integrations with other tools that focus on model serving.

## How to learn more about the project

We have a [documentation](https://docs.polyaxon.com/) that covers how to install and use Polyaxon.
Our code is open source and can be found [here](https://docs.polyaxon.com/).
You can also check this [demo video](https://www.youtube.com/watch?v=Iexwrka_hys)
from PyData about how to scale deep and reproduce deep learning on Kubernetes with Polyaxon.

## I am getting Bad Request when loading the web UI or using the CLI

Please be patient, sometimes deploying with an ingress or a load balancer
can take some time before you can communicate with the API.


## How do I contribute

Contributions to this project must be accompanied by a Contributor License Agreement.
This simply gives us permission to use and redistribute your contributions as part of the project.

You generally only need to sign the CLA once,
so if you’ve already signed one (even if it was for a different project),
you probably don’t need to do it again.

Please make sure to read and observe our [Code of Conduct](https://github.com/polyaxon/polyaxon/blob/master/CODE_OF_CONDUCT.md) as well.

## What is Polyaxon Beacon

Polyaxon will periodically communicate with a remote beacon server.
This is utilized for a couple of things, primarily:

 * Getting information about the current version of Polyaxon
 * Retrieving important system notices

The following information is reported:

 * A unique installation ID
 * The version of Polyaxon
 * General anonymous statistics on the data pattern (such as errors, installation type, ...)

The data reported is minimal and it greatly helps the development team behind Polyaxon.
With that said, you can disable the beacon with the following setting:

```yaml
trackerBackend: "noop"
```



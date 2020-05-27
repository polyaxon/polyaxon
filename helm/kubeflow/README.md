# polyaxon-kubeflow

Native support of Kubeflow operators in Polyaxon


## Description

This repo aims to provide a set of Helm charts, maintained and supported by Polyaxon, to easily deploy Kubeflow operators.

Polyaxon's Kubeflow integration supports as well running jobs directly on a Kubeflow deployment if it exists.

To learn more about how you can easily switch backends for your distributed experiments, please look at the [integration page](https://docs.polyaxon.com/integrations/kubeflow/) in our documentation.

## Install

### Setup Helm

To install the TFJob operator make sure you have helm installed, please see this [guide](/docs/guides/setup-helm/).

### Namespace

If you are using the tfjobs in Polyaxon, please install the chart on the same namespace where you installed Polyaxon.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

### Polyaxon's charts repo

You can add the Polyaxon helm repository to your helm, so you can install Polyaxon and other charts provided by Polyaxon from it. 
This makes it easy to refer to the chart without having to use a long URL each time.

```bash
$ helm repo add polyaxon https://charts.polyaxon.com
$ helm repo update
```

### TFJob

```bash
helm install polyaxon/tfjob --name=plxtf --namespace=polyaxon
```

### PytorchJob

```bash
helm install polyaxon/pytorchjob --name=plxpytorch --namespace=polyaxon
```

### MpiJob 

```bash
helm install polyaxon/mpijob --name=plxmpi --namespace=polyaxon
````

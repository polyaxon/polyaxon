# polyaxon-kubeflow

Native support of Kubeflow operators in Polyaxon


## Description

This repo aims to provide a set of Helm charts, maintained and supported by Polyaxon, to easily deploy Kubeflow operators.

Polyaxon's Kubeflow integration supports as well running jobs directly on a Kubeflow deployment if it exists.

To learn more about how you can easily switch backends for your distributed experiments, please look at the [integration page](https://polyaxon.com/integrations/kubeflow/) in our documentation.

## Install

### Setup Helm

To install the TFJob operator make sure you have [Helm](https://helm.sh/docs/intro/install/) installed.

### Namespace

If you are using the tfjobs in Polyaxon, please install the chart on the same namespace where you installed Polyaxon.

```bash
$ kubectl create namespace polyaxon

namespace "polyaxon" created
```

### Polyaxon charts repo

You can add the Polyaxon charts repo repository to your helm, so you can install Polyaxon and other charts provided by Polyaxon from it. 
This makes it easy to refer to the chart without having to use a long URL each time.

```bash
$ helm repo add polyaxon https://charts.polyaxon.com
$ helm repo update
```

### TFJob

```bash
helm install plxtf polyaxon/tfjob --namespace=polyaxon
```

### PytorchJob

```bash
helm install plxpytorch polyaxon/pytorchjob --namespace=polyaxon
```

### MpiJob 

```bash
helm install plxmpi polyaxon/mpijob --namespace=polyaxon
````

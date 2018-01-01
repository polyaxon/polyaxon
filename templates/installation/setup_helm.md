[Helm](https://helm.sh/) is the official package manager for Kubernetes,
it's a useful tool to install, upgrade, and manage applications on a Kubernetes cluster.

You will be using Helm to install and manage Polyaxon on your cluster.

## Install Helm

The simplest way to install helm is to run Helm’s installer script at a terminal:

```bash
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
```

## Initialize Helm and grant RBAC

After installing helm on your machine, initialize helm on your Kubernetes cluster
(you can check the [instruction provided bu helm](https://github.com/kubernetes/helm/blob/master/docs/rbac.md)).

Run the commands:

```bash
$ kubectl --namespace kube-system create sa tiller
$ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
```

```bash
$ helm init --service-account tiller
```

This is only needed once per Kubernetes cluster.


## Verify Helm version

You can check that the Helm installed is compatible with Polyaxon

```bash
$ helm version
```

Make sure you have at least version 2.5!

If your Helm version is compatible, then it is time to [deploy polyaxon](deploy_polyaxon)

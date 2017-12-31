The helm chart used to install Polyaxon has a lot of options for you to tweak.
For a semi-complete list of the changes you can apply via your helm-chart,
see the [Polyaxon Helm Chart Configuration Reference](/reference_polyaxon_helm).


## Applying configuration changes

The general method to modify your Kubernetes deployment is to:

 1. Make a change to the config.yaml
 2. Run a helm upgrade:

```bash
$ helm upgrade <RELEASE_NAME> polyaxon-chart/polyaxon -f config.yaml
```

Where <RELEASE_NAME> is the parameter you passed to --name when installing polyaxon with helm install.
If you don’t remember it, you can probably find it by doing helm list.

  3. Wait for the upgrade to finish, and make sure that when you do
  `kubectl --namespace=<NAMESPACE> get pod` the hub and proxy pods are in Ready state.
  Your configuration change has been applied!

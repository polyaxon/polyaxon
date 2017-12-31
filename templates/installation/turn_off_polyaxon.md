When you are done with Polyaxon, you can turn off the deployment,
and depending on your persistence configuration you can find all your data saved for future deployments.

You can also decide to completely turn off Polyaxon and remove the namespace and computational resources.

## Stop/kill running experiments

Stop/delete any running experiments, to kill all associated running jobs, and therefor their Kubernetes pods.

```bash
$ polyaxon kill experiment 13
$ polyaxon kill experiment 19
```

## Delete Helm release

Delete the helm release. This deletes all resources that were created by helm to make your Polyaxon.

```bash
$ helm delete <RELEASE_NAME> --purge
```

If you used the default values the command will be,

```bash
$ helm delete polyaxon --purge
```

## Delete the namespace

Delete the namespace Polyaxon was installed in.
This deletes any disks that may have been created to store user’s logs|database,
and any IP addresses that may have been provisioned.

```bash
$ kubectl delete namespace <your-namespace>
```

If you used the default values the command will be,

```bash
$ kubectl delete namespace polyaxon
```

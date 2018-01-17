In order to use the storage created in the [previous secrions](kubernetes_on_azure),
we need to create 2 persistent claim volumes (PVC).

But before that, we need to create a Kubernetes `secret`.

1. Create a secret

Kubernetes needs credentials to access the file share.
These credentials are stored in a Kubernetes secret, which is referenced when creating a Kubernetes pod.
When creating a Kubernetes secret, the secret values must be base64 encoded.

```
$ echo -n $STORAGE_ACCOUNT_NAME | base64

$ echo -n $STORAGE_KEY | base64
```

Switch back to the cloned `polyaxon-examples` repo, and update the values of `azure-secret,ylm`

```bash
$ vi azure/azure-secret.yml
```

with the values generated with base64.

2. Use `kubectl` to create a namespace `polyaxon`

```bash
$ kubectl create namespace polyaxon
```

3. Use `kubectl` to create the secret.

```bash
$ kubectl create -f azure/azure-secret.yml -n polyaxon
```

4. Use `kubectl` to create the PVCs based on the shares created

```bash
$ kubectl create -f azure/data-pvc.yml -n polyaxon
```

```bash
$ kubectl create -f azure/data-pvc.yml -n polyaxon
```

Now we can train our experiments.

In order to create a Kubernetes cluster on GKE you will need gcloud CLI and kubectl.

## Clone repo

Please clone the [Polyaxon examples repo](https://github.com/polyaxon/polyaxon-examples)

```bash
$ git clone https://github.com/polyaxon/polyaxon-examples.git
```

## GKE Kubernetes cluster

1. Create a cluster:

    * You can use [google's console](https://console.cloud.google.com/kubernetes/list)

    * Or the following the command:

    ```bash
    $ gcloud beta container --project "polyaxon-test" clusters create "polyaxon-test" --zone "us-central1-a" --username "admin" --cluster-version "1.9.6-gke.1" --machine-type "n1-standard-2" --image-type "COS" --disk-size "10" --num-nodes "3" --network "default"
    ```

    if you wish to use GPU, you need to add `--accelerator type "nvidia-tesla-k80,count=1"`

2. Create 3 Single Node Filer (`data`, `outputs`, and `logs`)

   The [click-to-deploy single-node file server ](https://console.cloud.google.com/launcher/details/click-to-deploy-images/singlefs) provides a ZFS file server running on a single Google Compute Engine instance.

    You need to create 3 SNFs: `plx-data`, `plx-outputs`, `plx-logs` for the storage name please keep the default value `data` for all of them, and check enable NFS sharing.


3. Get the ip address of the filers:

    ```bash
    $ gcloud --project "polyaxon-test" compute instances describe plx-data-vm --zone=us-central1-b --format='value(networkInterfaces[0].networkIP)'
    $ gcloud --project "polyaxon-test" compute instances describe plx-outputs-vm --zone=us-central1-b --format='value(networkInterfaces[0].networkIP)'
    $ gcloud --project "polyaxon-test" compute instances describe plx-logs-vm --zone=us-central1-b --format='value(networkInterfaces[0].networkIP)'
    ```

4. Update polyaxon-example's PVCs with the correct ip addresses:

    ```bash
    $ cd /path/to/polyaxon-examples/
    ```

    ```bash
    $ vi gke/data-pvc.yml
    # And replace with right ip address

    $ vi gke/outputs-pvc.yml
    # And replace with right ip address

    $ vi gke/logs-pvc.yml
    # And replace with right ip address
    ```

5. Use kubectl to create a namespace polyaxon

    ```bash
    $ kubectl create namespace polyaxon
    ```

6. Use kubectl to create the PVCs based on the shares created


    ```bash
    $ kubectl create -f gke/data-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/outputs-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/logs-pvc.yml -n polyaxon
    ```

7. Initialize Helm and grant RBAC

    ```bash
    $ kubectl --namespace kube-system create sa tiller
    $ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
    $ helm init --service-account tiller
    ```

Now we can [train experiments with Polyaxon](training_experiments_on_polyaxon)

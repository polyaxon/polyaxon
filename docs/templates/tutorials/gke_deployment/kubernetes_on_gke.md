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

    You might need to use the correct project name and zone.

    if you wish to use GPU, you need to add `--accelerator type "nvidia-tesla-k80,count=1"`

2. Create a Single Node Filer:

    The [click-to-deploy single-node file server ](https://console.cloud.google.com/launcher/details/click-to-deploy-images/singlefs)
    provides a ZFS file server running on a single Google Compute Engine instance.

    You need to create a filer: `polyaxon-nfs`,
    and keep the default value `data`, and check `enable NFS sharing`. You can set the storage to 50GB for example.


3. Use ssh to create some folders for `data`, `logs`, `outputs`, `upload`, and `repos` under /data :

    ```bash
    $ gcloud --project "polyaxon-test" compute ssh --ssh-flag=-L3000:localhost:3000 --zone=us-central1-b polyaxon-nfs-vm
    ```

    ```bash
    $ cd /data
    $ mkdir -m 777 data
    $ mkdir -m 777 outputs
    $ mkdir -m 777 logs
    $ mkdir -m 777 repos
    $ mkdir -m 777 upload
    ```

    This is just a tutorial, please consult with your devops team on how to setup an NFS server with correct security.

4. Get the ip address of the filers:

    ```bash
    $ gcloud --project "polyaxon-test" compute instances describe polyaxon-nfs-vm --zone=us-central1-b --format='value(networkInterfaces[0].networkIP)'
    ```

    You might need to use the correct project name and zone.


5. Update polyaxon-example's PVCs with the correct ip addresses:

    ```bash
    $ cd /path/to/polyaxon-examples/
    ```

    ```bash
    $ vi gke/data-pvc.yml
    # And replace with the right ip address

    $ vi gke/outputs-pvc.yml
    # And replace with the right ip address

    $ vi gke/logs-pvc.yml
    # And replace with the right ip address

    $ vi gke/repos-pvc.yml
    # And replace with the right ip address

    $ vi gke/upload-pvc.yml
    # And replace with the right ip address
    ```

6. Use kubectl to create a namespace polyaxon

    ```bash
    $ kubectl create namespace polyaxon
    ```

7. Use kubectl to create the PVCs based on the shares created


    ```bash
    $ kubectl create -f gke/data-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/outputs-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/logs-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/upload-pvc.yml -n polyaxon
    ```

    ```bash
    $ kubectl create -f gke/repos-pvc.yml -n polyaxon
    ```

8. Initialize Helm and grant RBAC

    ```bash
    $ kubectl --namespace kube-system create sa tiller
    $ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
    $ helm init --service-account tiller
    ```

Now we can [train experiments with Polyaxon](training_experiments_on_polyaxon)

---
title: "Using Polyaxon on GKE with an NFS server"
title_link: "Using Polyaxon on GKE with an NFS server"
meta_title: "Deploying Polyaxon on GKE with an NFS servers - Tutorials"
meta_description: "Deploying Polyaxon on GKE with an NFS servers."
custom_excerpt: "Deploying Polyaxon on GKE with an NFS servers."
featured: false
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - tutorials
    - training
---

In order to create a Kubernetes cluster on GKE you will need gcloud CLI and kubectl.

## Clone the examples repo

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


3. Use ssh to create some folders for `data`, `logs`, `outputs`, and `repos` under /data :

    ```bash
    $ gcloud --project "polyaxon-test" compute ssh --ssh-flag=-L3000:localhost:3000 --zone=us-central1-b polyaxon-nfs-vm
    ```

    ```bash
    $ cd /data
    $ mkdir -m 777 data
    $ mkdir -m 777 outputs
    $ mkdir -m 777 logs
    $ mkdir -m 777 repos
    ```

    This is just a tutorial, please consult with your devops team on how to setup an NFS server with correct security.

4. Get the ip address of the filer:

    ```bash
    $ gcloud --project "polyaxon-test" compute instances describe polyaxon-nfs-vm --zone=us-central1-b --format='value(networkInterfaces[0].networkIP)'
    ```

    You might need to use the correct project name and zone.


5. Update polyaxon-example's PVCs with the correct ip addresses:

    ```bash
    $ cd /path/to/polyaxon-examples/
    ```
    -
    ```bash
    $ vi gke/data-pvc.yml
    # And replace with the right ip address

    $ vi gke/outputs-pvc.yml
    # And replace with the right ip address

    $ vi gke/logs-pvc.yml
    # And replace with the right ip address

    $ vi gke/repos-pvc.yml
    # And replace with the right ip address
    ```

6. Use kubectl to create a namespace polyaxon

    ```bash
    $ kubectl create namespace polyaxon
    ```

7. Use kubectl to create the PVCs based on the nfs server

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
    $ kubectl create -f gke/repos-pvc.yml -n polyaxon
    ```

8. Initialize Helm and grant RBAC

    ```bash
    $ kubectl --namespace kube-system create sa tiller
    $ kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
    $ helm init --service-account tiller
    ```

## Train experiments 

Before we can train our experiments we need to deploy Polyaxon.

1. Change to examples folder, and specifically to cifar10

    ```bash
    $ cd /path/to/polyaxon-examples/tensorflow/cifar10
    ```

2. Deploy Polyaxon

    Add polyaxon charts to helm.

    ```bash
    $ helm repo add polyaxon https://charts.polyaxon.com
    $ helm repo update
    ```

    Now you can install Polyaxon with the `gke/polyaxon-config.yml` file,
    it overrides the default values from Polyaxon, by adding the data and outputs `existingClaim`
    with the values we just created. It also sets the compatible NVidia paths with GPU nodes.

    ```bash
    $ helm install polyaxon/polyaxon --name=polyaxon --namespace=polyaxon -f ../../gke/polyaxon-config.yml
    ```

3. Configure Polyaxon-CLI

    When the deployment is finished, you will receive a list of instructions in order to configure the cli.

4. Login with the superuser created by Polyaxon

    the instructions will tell you the superuser's username and a command to get the password.

    ```bash
    $ polyaxon login --username=root --password=rootpassword
    ```

5. Create a project

    ```bash
    $ polyaxon project create --name=cifar10 --description='Train and evaluate a CIFAR-10 ResNet model on polyaxon'
    ```

6. Init the project

    ```bash
    $ polyaxon init cifar10
    ```

7. Create the first experiment

    Unless you copied the data manually to the data share created in the previous section,
    the first time you create an experiment, it will create the data.

    Start an experiment with the default `polyaxonfile.yml`

    ```bash
    $ polyaxon run -u
    ```

8. Watch the logs

    ```bash
    $ polyaxon experiment -xp 1 logs

      Building -- creating image -
      master.1 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/1', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      master.1 --   force_gpu_compatible: true
      master.1 -- }
    ```

9. Watch the resources

    When the experiment starts training, you can also watch the logs

    ```bash
    $ polyaxon experiment -xp 1 resources

      Job       Mem Usage / Limit    CPU% - CPUs
    --------  -------------------  ---------------
    master.1  1.26 Gb / 6.79 Gb    120.11% - 6
    ```
    

10. Run a distributed experiment

    ```bash
    $ polyaxon run -f polyaxonfile_distributed.yml -u
    ```


8. Watch the logs

    ```bash
    $ polyaxon experiment -xp 2 logs

      Building -- creating image -
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_3/: (?, 16, 16, 32)
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_4/: (?, 16, 16, 32)
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_5/: (?, 16, 16, 32)
      worker.3 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/2', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      worker.3 --   force_gpu_compatible: true
      worker.1 -- INFO:tensorflow:image after unit resnet/tower_0/stage_1/residual_v1_6/: (?, 16, 16, 32)
      worker.3 -- }
      worker.3 -- allow_soft_placement: true
      worker.3 -- , '_tf_random_seed': None, '_task_type': None, '_environment': 'local', '_is_chief': True, '_cluster_spec': <tensorflow.python.training.server_lib.ClusterSpec object at 0x7fc7e9f53850>, '_tf_config': gpu_options {
      worker.3 --   per_process_gpu_memory_fraction: 1.0
      worker.3 -- }
      worker.3 -- , '_num_worker_replicas': 0, '_task_id': 0, '_save_summary_steps': 100, '_save_checkpoints_steps': None, '_evaluation_master': '', '_keep_checkpoint_every_n_hours': 10000, '_master': '', '_log_step_count_steps': 100}
      master.1 -- INFO:tensorflow:Using config: {'_model_dir': '/outputs/root/cifar10/experiments/2', '_save_checkpoints_secs': 600, '_num_ps_replicas': 0, '_keep_checkpoint_max': 5, '_session_config': gpu_options {
      master.1 --   force_gpu_compatible: true
      master.1 -- }
      ...
      worker.2 -- INFO:tensorflow:Evaluation [2/100]
      worker.4 -- INFO:tensorflow:Evaluation [2/100]
      worker.2 -- INFO:tensorflow:Evaluation [3/100]
      worker.4 -- INFO:tensorflow:Evaluation [3/100]
      worker.2 -- INFO:tensorflow:Evaluation [4/100]
      worker.4 -- INFO:tensorflow:Evaluation [4/100]
      worker.2 -- INFO:tensorflow:Evaluation [5/100]
      worker.4 -- INFO:tensorflow:Evaluation [5/100]
      worker.2 -- INFO:tensorflow:Evaluation [6/100]
      worker.4 -- INFO:tensorflow:Evaluation [6/100]
      worker.2 -- INFO:tensorflow:Evaluation [7/100]
      worker.4 -- INFO:tensorflow:Evaluation [7/100]
      worker.2 -- INFO:tensorflow:Evaluation [8/100]
      worker.4 -- INFO:tensorflow:Evaluation [8/100]
      worker.2 -- INFO:tensorflow:Evaluation [9/100]
      worker.4 -- INFO:tensorflow:Evaluation [9/100]
    ```

9. Watch the resources

    When the experiment starts training, you can also watch the logs

    ```bash
    $ polyaxon experiment -xp 2 resources

    Job       Mem Usage / Total    CPU% - CPUs
    --------  -------------------  -------------
    master.1  1.23 Gb / 55.03 Gb   0.01% - 6
    worker.2  1.1 Gb / 6.79 Gb     73.33% - 2
    worker.3  1.26 Gb / 55.03 Gb   246.32% - 6
    worker.4  1.12 Gb / 6.79 Gb    67.03% - 2
    ps.5      1.21 Gb / 55.03 Gb   272.41% - 6
    ```

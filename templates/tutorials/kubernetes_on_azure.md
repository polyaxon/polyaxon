In order to create a Kubernetes cluster that supports GPUs,
we will use acs-engine to generate the template we need to deploy
a Kubernetes cluster with everything already configured.

## Install acs-engine

If you already have a GPU enabled cluster, you can skip this step.

We are going to use [acs-engine](https://github.com/Azure/acs-engine/) to deploy a custom GPU cluster.

Download [acs-engine](https://github.com/Azure/acs-engine/releases ) prebuilt binary for your platform of choice.
And make sure you have [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed already.


## Clone repo

Please clone the [Polyaxon examples repo](https://github.com/polyaxon/polyaxon-examples)

```bash
$ git clone https://github.com/polyaxon/polyaxon-examples.git
```

## Deploy cluster

Now we will deploy the custom cluster based on a template in the examples repo.

!!! note
    The cluster will container 3 nodes: 2 CPU nodes and 1 GPU node.
    Make sure your azure quota allows you to create the cluster.

1. Change to where `acs-engine` binary is:

    ```bash
    $ cd /path/to/your/acs-engine/binary/
    ```

2. Copy the cluster template from the cloned repo:

    ```bash
    $ cp /path/to/polyaxon-examples/azure/polyaxon_gpu_cluster.json .
    ```

3. Get your subscription id, and create some environment variables for your deployments (it will come handy in the future)

    ```bash
    SUBSCRIPTION_ID=[your subscription id]
    RESOURCE_GROUP=[your resource group name]  # e.g. POLYAXON_TEST
    LOCATION=[Azure region that includes GPUs, you can check here]  # e.g. eastus
    DNS_PREFIX=[your DNS prefix]  # e.g. polyaxon-test
    ```

    And also update the `polyaxon_gpu_cluster.json` with the correct values, please replace all `REPLACE ME` fields.

4. Run the following command on your terminal:

    ```bash
    $ ./acs-engine generate polyaxon_gpu_cluster.json
    ```

    This will generate the necessary Azure templates to deploy the cluster.

5. Authenticate to your azure account

    ```bash
    $ az login
    $ az account set --subscription $SUBSCRIPTION_ID
    ```

6. Create a group


    ```bash
    $ az group create \
      --name $RESOURCE_GROUP \
      --location $LOCATION
    ```

7. Create a deployment

    ```bash
    $ az group deployment create \
     --resource-group $RESOURCE_GROUP \
     --template-file "./_output/${DNS_PREFIX}/azuredeploy.json" \
     --parameters "./_output/${DNS_PREFIX}/azuredeploy.parameters.json"
    ```

    Now you have a Kubernetes cluster deployed. You need to enable your `kubectl` to communicate with the cluster.

8. Export the Kubernetes configuration (kubeconfig) file to be able to use the cluster

    ```bash
    $ export KUBECONFIG=/path/to/your/acs-engine/_output/${DNS_PREFIX}/kubeconfig/kubeconfig.${LOCATION}.json
    ```

9. To access your kubernetes Dashboard

    ```bash
    $ kubectl proxy
    ```

    Since we will be using some storage for the data and outputs on Polyaxon, we need some azure storage for that.

10. Export a storage account name

    ```bash
    $ STORAGE_ACCOUNT_NAME=[storage account name]
    ```

11. Create storage

    ```bash
    $ az storage account create --resource-group $RESOURCE_GROUP --sku Standard_LRS --name $STORAGE_ACCOUNT_NAME
    ```

12. Get the access key for the storage

    ```bash
    $ STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT_NAME --query "[0].value" -o tsv)
    ```

13. Create a data and output shares on this storage

    ```bash
    $ az storage share create --name data --account-name $STORAGE_ACCOUNT_NAME --account-key $STORAGE_KEY

    $ az storage share create --name outputs --account-name $STORAGE_ACCOUNT_NAME --account-key $STORAGE_KEY
    ```

If you have a Kubernetes cluster running and have data storage, please go to [create persistent volumes](persistent_volumes)

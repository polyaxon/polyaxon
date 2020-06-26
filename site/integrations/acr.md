---
title: "Azure Container Registry ACR"
meta_title: "Azure Container Registry ACR"
meta_description: "How to pull images from your private Azure Container Registry ACR registry. Use your Azure Container Registry ACR registry to start your machine learning and deep learning experiments on Kubernetes on Polyaxon."
custom_excerpt: "Azure Container Registry allows you to build, store, and manage images for all types of container deployments."
image: "../../content/images/integrations/acr.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - registries
featured: false
popularity: 0
visibility: public
status: published
---

Integrate your Azure Container Registry ACR with Polyaxon to start your machine learning and deep learning experiments on Kubernetes.

## Overview

You can easily add many private registries to Polyaxon to pull private images and use them when scheduling your deep learning and machine learning experiments on Kubernetes using Polyaxon.

## Create a service principle and ArcPush

To use Azure Container Registry (ACR), you will need to provide proper credentials. 
You can do so by creating a [Service Principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals) 
that has the [AcrPush](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#acrpush) role.

 1. Login to your Azure account:
    
    ```bash
    az login
    ```

 2. Select your chosen subscription:
 
    ```bash
    az account set -s <SUBSCRIPTION>
    ```

 3. If you do not have a Resource Group, then create one:
 
    ```bash
    az group create --name <RESOURCE_GROUP_NAME> --location <RESOURCE_GROUP_LOCATION> --output table
    ```    
    
    > <RESOURCE_GROUP_LOCATION> refers to a data centre region. See a list of regions [here](https://azure.microsoft.com/en-us/global-infrastructure/locations/).
    
 4. Create the ACR if not you don't have one already
 
    ```bash
    az acr create --name <ACR_NAME> --resource-group <RESOURCE_GROUP_NAME> --sku Basic --output table
    ```
 
 5. Login in the ACR:

    ```bash
    az acr login --name <ACR_NAME>
    ```
 
 6. Note down the AppID of the ACR:
 
    ```bash
    az acr show --name <ACR_NAME> --query "id" -o tsv
    ```
    
    We need this in order to assign the AcrPush role which will allow Polyaxon to push images to the registry. You can save this to a bash variable like so:
    
    ```bash
    ACR_ID=$(az acr show --name <ACR_NAME> --query "id" -o tsv)
    ```
    
 7. Create a Service Principal with the AcrPush role assignment:
 
    ```bash
    az ad sp create-for-rbac --name <SP_NAME> --role AcrPush --scope <ACR_ID>
    ```

    > <SP_NAME> is a recognisable name for your Service Principal

    > <ACR_ID> is the AppID we retrieved in step 6 above. You can replace this with ${ACR_ID} if you saved it to a bash variable.
    
    Note down the AppID and password that are output by this step. These are the login credentials Polyaxon will use to access the registry.

## Create a secret to allow access to ACR

In order to create a valid secret using the login credentials from previous step, you need to create base64 auth based on the AppID and password.

So using python you can do:

```python
import base64
base64.b64encode('principal_id:password}'.encode())
```

## Create an auths config file

```json
{
    "auths": {
        "https://<ACR_NAME>.azurecr.io": {
            "auth": "<BASE64_VALUE>"
        }
    }
}
```

## Create a secret with config.json as a name

```bash
kubectl create secret generic docker-conf --from-file=config.json=./config.json -n polyaxon
```

## Add the secret to the k8s_secrets catalog in Stores

In order to use secret that you created before, in Polyaxon's Stores > Secrets, create a new secret entry, and set name and K8S Ref to "docker-conf".
  
## Make this access as default

After creating the access you need to mark it as default, so that Polyaxon uses it for scheduling builds. 


## Using the secret for pull only

If you wish to only use this credential secret for pulling images and the in-cluster registry for pushing, you should leave the host field empty.

## You can allow the docker process to pull from different registries

To allow this access to pull from other registries, you can set as many other auths and credsStore.

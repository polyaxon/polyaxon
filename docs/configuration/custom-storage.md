---
title: "Customize Volumes(Data and Outputs)"
sub_link: "custom-volumes"
meta_title: "Customize Customize Volumes(Data and Outputs) in Polyaxon - Configuration"
meta_description: "Polyaxon allows to mount multiple data volumes and outputs as well as cloud storages."
tags:
    - configuration
    - polyaxon
    - kubernetes
    - docker-compose
    - environment
    - orchestration
    - volumes
    - s3
    - gcp
    - azure-storage
sidebar: "configuration"
---

Polyaxon allows to mount multiple data volumes and outputs as well as cloud storages,
this could be very useful for large teams who need either to scale or
to have different teams to access different volumes.

This section tries to explain how Polyaxon mounts these volumes for experiments and jobs.

## Chart Definition

The [helm reference](/references/polyaxon-helm-reference/#persistence) describes briefly the data and outputs persistence definitions,
and how you can mount volumes, both persistent claims, host paths, and cloud storages, here's the example coming from the ref:

```yaml
persistence:
  data:
    data1:
      mountPath: "/data/1"
      hostPath: "/path/to/data"
      readOnly: true
    data2:
      mountPath: "/data/2"
      existingClaim: "data-2-pvc"
    data-foo:
      mountPath: "/data/foo"
      existingClaim: "data-foo-pvc"
    data-gcs3:
      store: gcs
      bucket: gs://data-bucket
      secret: secret-name
      secretKey: secret-key
    data-s3:
      store: s3
      bucket: s3://data-bucket
      secret: secret-name
      secretKey: secret-key
    data-azure:
      store: azure
      bucket: wasbs://data-container@account.blob.core.windows.net/
      secret: secret-name
      secretKey: secret-key
  outputs:
    outputs1:
      mountPath: "/outputs/1"
      hostPath: "/path/to/outputs"
      readOnly: true
    outputs2:
      mountPath: "/outputs/2"
      existingClaim: "outputs-2-pvc"
    outputs-foo:
      mountPath: "/outputs/foo"
      existingClaim: "outputs-foo-pvc"
    outputs-gcs3:
      store: gcs
      bucket: gs://outputs-bucket
      secret: secret-name
      secretKey: secret-key
    outputs-s3:
      store: s3
      bucket: s3://outputs-bucket
      secret: secret-name
      secretKey: secret-key
    outputs-azure:
      store: azure
      bucket: wasbs://outputs-container@account.blob.core.windows.net/
      secret: secret-name
      secretKey: secret-key
```

For GCS, S3, and Azure Storage, you need to need to provide a secret with auth access to these storages.

## Scheduling

When the user defines a multi data and/or outputs volumes,
Polyaxon has a default behavior for mounting these volumes during the scheduling of the jobs and experiments,
unless the user override this default behavior in the polyaxonfiles.

### For data

If the polyaxonfile for running an experiment or a job does not define the data volume or volumes that it needs access to,
Polyaxon will by default mount all these volumes when it schedules the experiment or the job.

These data volumes will be accessible to you as a dictionary `{volume_name: path_to_data}`,
exported as an env variable `POLYAXON_RUN_DATA_PATHS`.

You can use as well our `tracking` api in `polyaxon-client` to get access to this env variable automatically.

If on the other hand, you wish to only mount one volume or a subset of the volumes,
you then need to provide this information in the polyaxonfile, e.g.

```yaml
environment:
  persistence:
    data: ['data1', 'data-foo']
```

By providing this persistence subsection,
Polyaxon will only mount these volumes by looking up there names from the defined volumes.


### For outputs

Polyaxon mounts only one  outputs for a particular experiment or a job.

If the polyaxonfile for running an experiment or a job does not define the outputs volume,
Polyaxon will, by default mount one volume, either the first one or a random one from the list of the defined volumes.

The outputs volume will be accessible to you as a string `path_to_outputs_for_experiment`,
exported as an env variable `POLYAXON_RUN_OUTPUTS_PATH`.

You can use as well our `tracking` api in `polyaxon-client` to get access to this env variable automatically.

If on the other hand, you wish to mount a particular volume,
you then need to provide this information in the polyaxonfile, e.g.

```yaml
environment:
  persistence:
    outputs: 'outputs-foo'
```

By providing this persistence subsection,
Polyaxon will mount the volume by looking up the name from the defined volumes.


## Cloud storages

In order to mount a cloud storage, 
users need to provide authentication access to Polyaxon for all storages needed during the scheduling.

The way to do that is by creating a secret of your cloud storage access auth, 
and providing the secret name and key name to use from that secret. 
(You can use the same k8s secret to manage multiple storage access auth, in this case only the key will be different).   

### For Google Cloud Storage

Google cloud storage provide an easy way to download access key as json file. 
You should create a secret based on that json file.

`kubectl create secret generic gcs-secret --from-file=key.json=path/key.json -n polyaxon`

Polyaxon client does not bundle by default the google cloud requirements to keep the client lightweight, 
the user need to add a `pip install google-cloud-storage`

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install google-cloud-storage
``` 


### For S3

In order to use S3 buckets with Polyaxon, you should create a file containing you access information json object, e.g. `key.json`.
This file should include at least the following information:

```json
{
  "AWS_ACCESS_KEY_ID" : "",
  "AWS_SECRET_ACCESS_KEY": ""
}
```

All possible values:

```json
{
  "AWS_ENDPOINT_URL": "",
  "AWS_ACCESS_KEY_ID": "",
  "AWS_SECRET_ACCESS_KEY": "",
  "AWS_SECURITY_TOKEN": "",
  "AWS_REGION": ""
}
```

`kubectl create secret generic s3-secret --from-file=key.json=path/key.json -n polyaxon`


Polyaxon client does not bundle by default the boto requirements to keep the client lightweight, 
the user need to add the necessary steps to be available during the run:

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install boto3
    - pip3 install botocore
``` 


### For Azure storage

You should create a storage account (e.g. plx-storage) and a blob (e.g. outputs). 
You should then create a file you access information json object, e.g. `key.json`. 
This file should include the following information:

```json
{ 
  "AZURE_ACCOUNT_NAME": "plx-storage",
  "AZURE_ACCOUNT_KEY": "your key",
  "AZURE_CONNECTION_STRING": "your connection string",
}
```

`kubectl create secret generic az-secret --from-file=key.json=path/key.json -n polyaxon`


Polyaxon client does not bundle by default the azure storage requirements to keep the client lightweight, 
the user need to add the necessary steps to be available during the run:

```yaml
build:
  ...
  build_steps:
    ...
    - pip3 install azure-storage
``` 

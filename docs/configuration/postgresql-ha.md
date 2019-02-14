---
title: "PostgreSQL HA"
sub_link: "postgresql-ha"
meta_title: "High availability of postgresql database in Polyaxon - Configuration"
meta_description: "Keeping database records of your users, projects, experiments, and jobs is very important. Polyaxon offers a couple of ways to set a high available database."
tags:
    - configuration
    - polyaxon
    - postgresql
    - scaling
    - high-availability
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

Since keeping database records of your users, projects, experiments, and jobs is very important.
Polyaxon offers a couple of ways to set a high available database.

## Persistence

The easiest way to keep your database intact in case of node failures or restarts,
is by enabling postgresql persistence, enabling persistence will tell the database to use
a persistent volume to store data instead of using the host node.

### Dynamic persistence provisioning

Here's an example of using dynamic provisioning:

```yaml
postgresql:
  persistence:
    enabled: true
    size: 5Gi
```

Using this configuration, the volume will be provisioned dynamically,
based on default storage class defined in your cluster.

### Existing PersistentVolumeClaims

In case you want to have more control where and how the persistence claims is created,
and should not be managed by the chart,
you need to define a PVC and assign it to the `persistence.existingClaim`.

 1. Create the PersistentVolume
 2. Create the PersistentVolumeClaim
 3. Use the name of this claim in the chart

    ```yaml
    postgresql:
      persistence:
        enabled: true
        existingClaim: myClaimName
    ```

## External postgresql

If you prefer to have the postgresql database managed and hosted outside of Kubernetes,
instead of the in-cluster one provided by Polyaxon, e.g.
[Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/),
[Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/services/postgresql/), 
[GCP Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres/), 
or [DigitalOcean managed PostgreSQL](https://www.digitalocean.com/products/managed-databases/).
You need to disable the in-cluster database, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
postgresql:
  enabled: false
  postgresUser: polyaxon
  postgresPassword: polyaxon
  postgresDatabase: postgres
  externalPostgresHost: 35.262.163.88
```

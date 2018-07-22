Since keeping database records of your users, projects, experiments, and jobs is very important.
Polyaxon offers a couple of ways to preserve your database:

## Persistence

The easiest way to keep your database intact in case of node failures or restarts,
is by enabling postgresql persistence, enabling persistence will tell the database to you use
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

If you prefer to have the postgresql managed and hosted outside of Kubernetes,
instead of the in-cluster one provided by Polyaxon, e.g.
[Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/services/postgresql/),
[Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/), or [GCP Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres/).
You need to disable in-cluster database, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
postgresql:
  enabled: false
  postgresUser: polyaxon
  postgresPassword: polyaxon
  postgresDatabase: postgres
  externalPostgresHost: 35.262.163.88
```

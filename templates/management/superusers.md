Superusers in Polyaxon are allowed to:

 * Access all projects in read/write mode.
 * Accept new users to use polyaxon on your cluster.
 * Grant access to new users.
 * Perform cluster management.


## Default Superuser

Polyaxon comes with a default superuser `root`. This user has also a default password and email.

You can customize the `username`, `email`, and `password` of that user by updating your `config.yaml`.

!!! info
    For more details about how to extend your polyaxon deployment, go to [extend deployment section](/customization/extend_deployments).

If null password is provided for this default user, Polyaxon will generate a random password.
The admin of your cluster will be able to see it by running the command provided
in the notes after a successful [deployment of Polyaxon](/installation/deploy_polyaxon).

## Accept/Reject new user

Superuser are also responsible for managing who can use the platform,
therefor they are responsible to accept or reject new users.

To accept a new user, run the following command

```bash
$ polyaxon user activate <USERNAME>
```

To reject a new user, run the following command

```bash
$ polyaxon user reject <USERNAME>
```


## Grant/Revoke superuser role

Superusers can also grant other users the `superuser` role.

To grant a user the `superuser` role, run the following command

```bash
$ polyaxon superuser grant <USERNAME>
```

To revoke a user the `superuser` role, run the following command

```bash
$ polyaxon superuser revoke <USERNAME>
```

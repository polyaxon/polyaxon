This section describes how to manage users and their permissions on Polyaxon.

This version of Polyaxon has currently two type of users:

 * [Superusers](superusers)
 * [Normal users](users)

!!! attention "Teams"
    We are currently working on a new version of Polyaxon with teams,
    which will introduce more roles and access levels
    to manage teams, resources quotas, and parallelism quotas.

By default, Polyaxon ships with a default super user `root`.
You can customize the `username`, `email`, and `password` of that user by updating your `config.yml`.

!!! info
    For more details about how to extend your polyaxon deployment, go to the [extend deployment section](/customization/extend_deployments).

If null password is provided for this default user, Polyaxon will generate a random password.
The admin of your cluster will be able to see it by running the command provided
in the notes after a successful [deployment of Polyaxon](/installation/deploy_polyaxon).

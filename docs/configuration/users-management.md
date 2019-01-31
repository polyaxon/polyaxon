---
title: "Users Management"
sub_link: "users-management"
meta_title: "Users & Permissions in Polyaxon - Configuration"
meta_description: "Polyaxon has built-in superuser and users permissions to allow teams to collaborate effectively. Learn more about user permissions in Polyaxon."
tags:
    - configuration
    - polyaxon
    - management
    - users
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

This section describes how to manage users and their permissions on Polyaxon.

Polyaxon CE has two type of users:

 * Superusers
 * Normal users

> If you need more granular roles and permissions 
to reflect your organization and teams structure you should check our enterprise offering.

## Superuser

By default, Polyaxon ships with a default super user `root`.
You can customize the `username`, `email`, and `password` of that user by updating your `config.yml`.

Here's the default values: 

```yaml
user:
  username: root
  email: root@polyaxon.local
  password: rootpassword
```

If the password provided is null, i.e. `password:`, Polyaxon will generate a random hash password that the cluster admin will be able to get after a successful deployment.

The superuser role has many privileges:

 * Access all projects in read/write mode.
 * Accept new users to Polyaxon.
 * Delete users from Polyaxon.
 * Can promote other users to the superusers role.
 * Perform cluster management.
 * Can access an admin view if activated.
 

### Accept/Reject new user

Superuser are responsible for managing who can use the platform,
therefor they are responsible to accept or reject new users.

To accept a new user, run the following command

```bash
$ polyaxon user activate <USERNAME>
```

To reject a new user, run the following command

```bash
$ polyaxon user reject <USERNAME>
```


### Grant/Revoke superuser role

Superusers can also grant other users the `superuser` role.

To grant a user the `superuser` role, run the following command

```bash
$ polyaxon superuser grant <USERNAME>
```

To revoke a user the `superuser` role, run the following command

```bash
$ polyaxon superuser revoke <USERNAME>
```


## Users

Normal users in Polyaxon are only allowed to access in read/write mode their own projects and experiments,
additionally they can access in read mode public projects from other users.


### New user creation process

The process to create a new user is the following:

 1. The new user creates an account on the Polyaxon Dashboard `HOST:PORT/users/register`.
 2. The new user must contact a superuser.
 3. A superuser accepts/rejects the new user.
 4. Optionally the superuser grants the `superuser` mode to the new user.

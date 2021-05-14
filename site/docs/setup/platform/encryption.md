---
title: "Encryption configuration"
sub_link: "platform/encryption"
meta_title: "Encryption configuration in Polyaxon - Configuration"
meta_description: "Polyaxon's Encryption configuration."
tags:
  - configuration
  - polyaxon
  - kubernetes
  - docker-compose
sidebar: "setup"
---

Polyaxon might need to save some sensitive information in the database, such as keys.

By default Polyaxon uses Kubernetes secrets for accessing all user's provided secrets,
but sometimes it might need to also store some additional information.
The way Polyaxon does it is by obfuscating the data and then applying an encryption
to the values based on Fernet before saving the information.

## Create a secret containing an encryption key

In order to enable the encryption, the user must provide an encryption secret,
the secret must contain at least one item `POLYAXON_ENCRYPTION_SECRET`.

You can use this to generate a valid secret:

```python
Fernet.generate_key()
```

> N.B. Please you should know that changing the secret will lock access to any previously saved value in the DB,
> You need to delete previous values and set new ones

## Enable encryption

Update your deployment config file with the encryption secret:

```yaml
encryptionSecret: my-secret
```

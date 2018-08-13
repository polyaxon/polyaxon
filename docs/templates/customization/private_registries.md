Polyaxon allows to define images from private Container Registries

As an example, let's assume that you want to use the `registry.example.com/private/image:v1.1` image
which is private and requires you to login into a private container registry.

Let's also assume that these are the login credentials:

Key | value
-------|------
  registry| registry.example.com
  username| my_username
  password| my_password

To configure access for `registry.example.com`, you need to add the registry to your configuration based on our URI spec:

`"user:passowrd@host:port"` or `"user:passowrd@site.com"`

In the case of the example you need to add your container registry to deployment configuration:

```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
```

Polyaxon will turn this uri specification into a secret and expose it to the necessary service
responsible for building your experiment/job images.

You can have more than one private container registry defined in your Polyaxon deployment configuration:

```yaml
privateRegistries:
  - "my_username:my_password@registry.example.com"
  - "my_username2:my_password2@registry:5000"
```

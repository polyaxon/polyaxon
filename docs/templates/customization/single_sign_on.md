Single Sign-On (or SSO) allows you to manage your organization’s entire membership via a third party provider.

# Behaviour

Supports multiple authentication schemes:

  * Signup/login with username/e-mail and password
  * Signup with LDAP
  * Signup/Login with Github accounts
  * Signup/Login with Gitlab accounts
  * Signup/Login with Bitbucket accounts
  * Connecting more than one social account to an account based on email/username

## Default Membership

Every member who creates a new account via SSO will be given access to the platform with a user role.

## Providers

### LDAP

In order to use LDAP with Polyaxon you need to provide a list of configuration parameters during the deployment:

```yaml
auth:
  ldap:
    enabled: true
    serverUri:
    globalOptions: {}
    connectionOptions: {}
    bindDN:
    bindPassword:
    userSearchBaseDN:
    userSearchFilterStr:
    userDNTemplate:
    startTLS: false
    userAttrMap: {}
    groupSearchBaseDN:
    groupSearchGroupType:
    requireGroup:
    denyGroup:
```

### Github

You need to register a new [application on github](https://github.com/settings/applications/new).

You should provide a callback URL: [Domain/IP]`/oauth/github`

And use your client id and secret token during the deployment:

```yaml
auth:
  github:
    enabled: true
    clientId:
    clientSecret:
```


### Gitlab

You need to register a new [application on gitlab](http://doc.gitlab.com/ce/integration/oauth_provider.html).

You should provide a callback URL: [Domain/IP]`/oauth/gitlab`

And use your client id and secret token during the deployment:

```yaml
auth:
  gitlab:
    enabled: true
    clientId:
    clientSecret:
```

If you have an on-premise Gitlab installation you can additionally provide your Gitlab url:


```yaml
auth:
  gitlab:
    enabled: true
    clientId:
    clientSecret:
    url:
```


### Bitbucket

You need to register a new [application on bitbucket](https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html).

You should provide a callback URL: [Domain/IP]`/oauth/bitbucket`

And use your client id and secret token during the deployment:

```yaml
auth:
  bitbucket:
    enabled: true
    clientId:
    clientSecret:
```


## Signup/Login

Once you set one or all of these providers your users will be able to signup/login based on any of these providers.

### Signup page

![signup](/images/dashboard/signup.png)

### Login page
![login](/images/dashboard/login.png)

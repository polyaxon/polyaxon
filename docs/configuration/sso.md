---
title: "Single Sign On"
sub_link: "sso"
meta_title: "Single Sign On in Polyaxon - Configuration"
meta_description: "Polyaxon has built-in single sign on for offloading users' creation process to a third party system."
tags:
    - configuration
    - polyaxon
    - management
    - users
    - sso
    - kubernetes
    - docker-compose
sidebar: "configuration"
---
Single Sign-On (or SSO) allows you to manage your organization’s entire membership via a third party provider.

# Behaviour

Supports multiple authentication schemes:

  * Signup/login with username/e-mail and password
  * Signup with LDAP
  * Signup/Login with Github accounts
  * Signup/Login with Gitlab accounts
  * Signup/Login with Bitbucket accounts
  * Signup/Login with Microsoft (Office 365, Azure) accounts
  * Connecting more than one social account to an account based on email/username

## Default Membership

Every member who creates a new account via SSO will be inactive, and can access to the platform with a user role after activation by a superuser.

## Providers

### LDAP

In order to use LDAP with Polyaxon you need to provide a list of configuration parameters during the deployment:

```yaml
auth:
  ldap:
    enabled: true
    serverUri:  # e.g. "ldap://my.ldapserver.com"
    globalOptions: {}
    connectionOptions: {}
    bindDN:
    bindPassword:
    userSearchBaseDN:  # e.g. "dc=domain,dc=com"
    userSearchFilterStr:  # e.g. "(mail=%(user)s)"
    userDNTemplate:  # e.g. "uid=%(user)s,ou=users,dc=example,dc=com"
    startTLS: false
    userAttrMap: {}  # e.g. {"first_name": "givenName", "last_name": "sn"}
    groupSearchBaseDN:  # e.g. "ou=groups,dc=example,dc=com"
    groupSearchGroupType:  # e.g. "(objectClass=groupOfNames)"
    requireGroup:  # e.g. "cn=enabled,ou=groups,dc=example,dc=com"
    denyGroup:  # e.g. "cn=disabled,ou=groups,dc=example,dc=com"
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

### Microsoft (Azure)

You need to register a new [application on Azure](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-integrating-applications).

You will need to provide a reply URL: [Domain/IP]`/oauth/azure`

And use your client id and secret token during the deployment:

```yaml
auth:
  azure:
    enabled: true
    tenantId:
    clientId:
    clientSecret:
```

## Signup/Login

Once you set one or all of these providers your users will be able to signup/login based on any of these providers.

### Signup page

![signup](../../content/images/concepts/dashboard/signup.png)

### Login page
![login](../../content/images/concepts/dashboard/login.png)

---
title: "Polyaxon Security"
sub_link: "security"
meta_title: "Polyaxon Security - Core Concepts"
meta_description: "Polyaxon is committed to developing secure, reliable products utilizing all modern security best practices. Find out more!"
visibility: public
status: published
tags:
  - reference
  - polyaxon
  - kubernetes
  - deep-learning
  - machine-learning
  - security
---

Polyaxon is committed to developing secure, reliable products utilizing all modern security best practices and processes.

We take security very seriously at Polyaxon and welcome any peer review of our [open-source codebase](https://github.com/polyaxon/polyaxon) to help ensure that it remains completely secure.


## Security features

### SSL

Polyaxon allows and recommends setting an SSL for your deployments.

### Admin view

The admin view is disabled by default, and can be easily enabled.

### Data validation and serialization

Polyaxon performs strong serialization and validation on all data that goes into the database, and follows industry best practices when uploading files.

### Encoded tokens everywhere

All user invitation and password reset tokens are base64 encoded with serverside secret. All tokens are always single use and always expire.

### Password hashing

Polyaxon follows best practices for authentication with all passwords hashed and salted properly to ensure password integrity.

### SQLi prevention

Polyaxon core API runs on django, and uses it's ORM for creating queries, there's no query builder and we do not generate raw SQL queries with interoperable variables.

### XSS prevention

Polyaxon uses safe/escaped strings used everywhere.

### Dependency management

All dependencies used in Polyaxon are scanned and reviewed carefully.


## Responsible disclosure guidelines

We invite any Polyaxon user to take part in responsible disclosure of any vulnerability.

- Provide details of the vulnerability, including information needed to reproduce and validate the vulnerability and a Proof of Concept
- Make a good faith effort to avoid privacy violations, destruction and modification of data
- Give reasonable time to correct the issue before making any information public

Security issues always take precedence over bug fixes and feature work. We can and we will make expedite releases/patches mark releases for serious security issues.

## Issue triage

We're always interested in hearing about any reproducible vulnerability that affects the security of Polyaxon users, including...

- Cross Site Scripting (XSS)
- Cross Site Request Forgery (CSRF)
- Server Side Request Forgery (SSRF)
- Remote Code Execution (RCE)
- SQL Injection (SQLi)

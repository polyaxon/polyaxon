## login


Usage:

```bash
$ polyaxon login [OPTIONS]
```

### Example using username and password

```bash
$ polyaxon login --username=adam --password=secret
```

### Example using username and prompt

```bash
$ polyaxon login --username=adam

Please enter your password:
```

### Example using token

```bash
$ polyaxon login --token=my-token
```

Login to Polyaxon.

Options:

option | type | description
-------|------|------------
  -t --token| TEXT|     Polyaxon token
  -u --username| TEXT|  Polyaxon username
  -p --password| TEXT|  Polyaxon password
  --help| |Show this message and exit.


## logout

Usage:

```bash
$ polyaxon logout
```

Logout of Polyaxon.


## whoami

Usage:

```
$ polyaxon whoami
```

Show current logged Polyaxon user.

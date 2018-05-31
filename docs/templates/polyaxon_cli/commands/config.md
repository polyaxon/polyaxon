Set and get global configurations.

## Get global config by keys

Usage:

```basg
$ polyaxon config get [OPTIONS] [KEYS]...
```

Get the global config values by keys.

Example:

```bash
$ polyaxon config get host http-port
```

## Set global config keys

Usage:

```bash
$ polyaxon config set [OPTIONS]
```

Set the global config values.

Example:

```bash
$ polyaxon config set --host=localhost http_port=80
```

Options:

option | type | description
-------|------|------------
  --verbose| BOOLEAN | To set the verbosity of the client.
  --host| TEXT | To set the server endpoint.
  --http-port| INTEGER | To set the http port.
  --ws-port| INTEGER | To set the stream port.
  --use-https| BOOLEAN | To set the https.
  --help| | Show this message and exit..

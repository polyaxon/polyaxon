Polyaxon CLI is python command line interface to interact with Polyaxon API.


## Install

To install it simply run:

```bash
pip install -U polyaxon-cli
```

and to install the CLI for python3 usage

```bash
pip3 install -U polyaxon-cli
```


## Configure

In order for polyaxon CLI to work correctly,
you must execute the steps from [polyaxon helm deployments](deploy_polyaxon).

Those steps ensures that, you configure Polyaxon to connect to the correct host, on the correct ports.


After installing the CLI you can view the commands supported using the `--help` option.

```bash
$ polyaxon --help
```

For more information please have a look at some [assumptions and conventions](/polyaxon_cli/assumptions)
Polyaxon use for it's [commands](/polyaxon_cli/commands)

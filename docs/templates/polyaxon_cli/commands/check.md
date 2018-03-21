Check the validity of a polyaxonfile.yml.

Usage:
```bash
$ polyaxon check [OPTIONS]
```

Check a polyaxonfile.

Options:

option| type | description
------|------|------------
  -f, --file| PATH| The polyaxon file to check.
  -a, --all| | Checks and prints the validated file.
  -v, --version| | Checks and prints the version.
  --run-type| | Checks and prints the run_type.
  -p, --project| | Checks and prints the project def.
  --log-path| | Checks and prints the log path.
  -x, --experiments| | Checks and prints the matrix space of experiments.
  -m, --matrix| | Checks and prints the matrix def.
  --help| | Show this message and exit.

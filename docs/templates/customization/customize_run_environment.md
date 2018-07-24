Usually a docker image specifies the functionality and environment
that you wish to run your experiments.

The following sections will describe how to use existing docker images and how to create custom images.

## Public images

You can use any docker image available on a public registry to run your experiments.

You can also build your custom docker images and push them to a public registry and use them on Polyaxon.


## Custom images

Alternatively, you can use the polyaxonfile to define how to customize a public image to your need,
and Polyaxon will take care of building the image before running your code.

For example

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```

### Environment variables

To expose some environment variables you can use `env_vars`

For example

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn
  env_vars:
    - ['MY_ENV_VAR_KEY1', 'MY_ENV_VAR_VALUE1']
    - ['MY_ENV_VAR_KEY2', 'MY_ENV_VAR_VALUE2']

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```

### Installing libraries with pip

Polyaxon also provides, an easy way to install multiple python libraries:

 1. you can define a requirements file; the name must be either `requirements.txt` or `polyaxon_requirements.txt`


    ```bash
    $ vi polyaxon_requirements.txt
    ...
    ```

 2. a command `pip install -r polyaxon_requirements.txt` to install the requirements


    ```yaml
    ---
    version: 1

    kind: experiment

    declarations:
      batch_size: 128
      lr: 0.1

    build:
      image: tensorflow/tensorflow:1.4.1-py3
      build_steps:
        - pip install -r polyaxon_requirements.txt

    run:
      cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
    ```

### Installing other libraries or running other commands

You can also install or execute other commands, by adding them to the `build_steps` part.
If you have multiple commands that you wish to execute,
You can create an executable file, the filename must be `polyaxon_setup.sh` or `setup.sh`, and a command to execute that file `./polyaxon_setup.sh`.

```yaml

---
version: 1

kind: experiment

declarations:
  batch_size: 128
  lr: 0.1

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - ./polyaxon_setup.sh

run:
  cmd: python3 train.py --batch_size={{ batch_size }} --lr={{ lr }}
```


### Running a script


In some case you will need to change the directory before running a command,
or you might need to run multiple commands,
the best way to do that is to create an executable file,
e.g. `run.sh` where you will put all the commands you wish to run, and then just run that file:

For example the `run.sh` could be:

```bash
cd to_some_path; echo "running my run.sh file"; python model.py
```

And your cmd in polyaxonfile:

```yaml
run:
  cmd: /bin/bash run.sh
```

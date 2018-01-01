Usually a docker image specifies the functionality and environment that you wish when running your experiments.

The following sections will describe how to use existing docker images and how to create custom images.

## Public images

You can use any docker image available on a public registry to run you experiments.

You can also build your custom docker images and push them to a public registry and use them on Polyaxon.


## Custom images

Alternatively, you can use the polyaxonfile to define how to customize a public image to your need,
and Polyaxon will take care of building the image before running your code.

For example

```yaml
---
version: 1

project:
  name: mnist

declarations:
  batch_size: 128
  lr: 0.1

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

Polyaxon also provides, an easy way to install multiple python libraries:

 1. you can define a `polyaxon_requirements.txt` file


    ```bash
    $ vi polyaxon_requirements.txt
    ...
    ```

 2. a command `pip install -r polyaxon_requirements.txt` int he to install our requirements


    ```yaml
    ---
    version: 1

    project:
      name: mnist

    declarations:
      batch_size: 128
      lr: 0.1

    run:
      image: tensorflow/tensorflow:1.4.1-py3
      steps:
        - pip install -r polyaxon_requirements.txt
      cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
    ```


You can also install or execute other commands, by adding them to the `steps` part.
If you have multiple commands that you wish to execute,
Polyaxon allows you to specify a `polyaxon_setup.sh` file, and a command to execute that file `./polyaxon_setup.sh`.

```yaml
---
version: 1

project:
  name: mnist

declarations:
  batch_size: 128
  lr: 0.1

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - ./polyaxon_setup.sh
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

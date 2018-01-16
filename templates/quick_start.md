# Polyaxon with an introductory example


Let’s look at an example of how you can use Polyaxon for your deep learning experiments.
This example assumes that both Polyaxon is [installed](installation/introduction) and running.
And you are logged in to your Polyaxon account through the [polyaxon-cli](polyaxon_cli/commands/auth)

1. The first step is to create a project, you can do that with the `Polyaxon-dashboard` or with the `polyaxon-cli`

    ```bash
    $ polyaxon project create --name=quick-start --description='Polyaxon quick start.'
    ```

2. Head to your terminal and clone our [quick-start repo](https://github.com/polyaxon/polyaxon-quick-start)

    ```bash
    $ git clone https://github.com/polyaxon/polyaxon-quick-start.git
    ...

    $ cd polyaxon-quick-start
    $ ls polyaxon-quick-start

    mnsit.py README.me LICENSE
    ```

3. Initialize the project with the same name that you used when you created the project in Polyaxon

    ```bash
    $ polyaxon init quick-start

    Polyaxonfile was created successfully `polyaxonfile.yml`
    ```

4. Let's open the created `polyaxon.yml`, since we cloned the project,
   this file is already populated with the minimum configuration needed to start an experiment:

    ```yaml
    ---
    version: 1

    project:
      name: quick-start

    run:
      image: tensorflow/tensorflow:1.4.1-py3
      steps:
        - apt-get -y update && apt-get -y install git
        - pip3 install --no-cache-dir -U -e git+https://github.com/polyaxon/polyaxon-helper.git@master#egg=polyaxon-helper
      cmd: python model.py
    ```

    This configuration specifies:

       * The Polyaxon specification `version` we are using.
       * The `project` namespace we want to run the experiment inside.
       * The `run` section to build and execute our code,
         in this case we want to run our code with this tensorflow specific docker image.
         We are also install the polyaxon helper library to send metrics at the end of the experiment.

5. Now let's upload our code to create a commit on Polyaxon

    ```bash
    $ polyaxon upload
    ```

6. Then start the experiment

    ```bash
    $ polyaxon run

    Experiment was created
    ```

!!! tip
    You can merge these 2 steps: `polyaxon run -u`

7. Check your project experiments list

    ```bash
    $ polyaxon project experiments
    ```

    sequence | name | user | project | status | created_at
    ---------|------|------|---------|--------|-----------
    1 | root.quick-start.1 | root | root.quick-start| Scheduled | seconds ago


8. Check the experiment logs and resource

    Info:

    ```bash
    $ polyaxon experiment -xp 1 get

    Experiment info:

    ---------------------  ------------------
    sequence               1
    unique_name            root.quick-start.1
    user                   root
    project_name           root.quick-start
    experiment_group_name
    last_status            Building
    created_at             a few seconds ago
    is_clone               False
    num_jobs               0
    finished_at
    started_at
    ---------------------  ------------------
    ...
    ```

    Logs:

    ```bash
    $ polyaxon experiment -xp 1 logs
    Building -- creating image -
    INFO:tensorflow:global_step/sec: 1.59552
    INFO:tensorflow:loss = 0.116677, step = 101 (62.679 sec)
    INFO:tensorflow:global_step/sec: 1.47121
    INFO:tensorflow:loss = 0.0842577, step = 201 (67.969 sec)
    ...
    ```

    Resources:

    ```bash
    $ polyaxon experiment -xp 1 resources

        Job                           Mem Usage / Limit    CPU% - CPUs
    --------------------------------  -------------------  ---------------
    36f277f5053f511f97ae39dc6e00691f  0.47 Gb / 6.79 Gb    120.47% - 6
    ...
    ```

8. More information about the experiment in the dashboard

    ```bash
    $ polyaxon dashboard

    Dashboard page will now open in your browser. Continue? [Y/n]: y
    ```

9. Finally, Let start tensorboard to see the model outputs:

     ```bash
     $ polyaxon project start_tensorboard
     ```

Congratulations! You've trained your first experiment with Polyaxon. Behind the scene a couple of things have happened:

 * You uploaded your code, and created a git commit for this version of your code
 * You built a docker image with the latest version of your code
 * You ran the image with the specified command in the polyaxonfile
 * You persisted your logs and outputs to your volume claims

To gain a deeper understanding on how polyaxon can help you iterate faster with your experiments,
please take some time to familiarize yourself with the [experimentation workflow](experimentation/concepts)

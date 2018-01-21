# Polyaxon with an introductory example


Let’s look at an example of how you can use Polyaxon for your deep learning experiments.
This example assumes that both Polyaxon is [installed](installation/introduction) and running.
And you are logged in to your Polyaxon account through the [polyaxon-cli](polyaxon_cli/commands/auth)


1. The first step is to check that polyaxon is reporting your cluster correctly

    ```bash
    $ polyaxon cluster


    Cluster info:

    --------------  ----------------------------------------
    build_date      2017-11-20T05:17:43Z
    major           1
    go_version      go1.8.3
    git_version     v1.8.4
    platform        linux/amd64
    git_commit      9befc2b8928a9426501d3bf62f72849d5cbcd5a3
    git_tree_state  clean
    minor           8
    compiler        gc
    --------------  ----------------------------------------

    Cluster Nodes:

      sequence  name                       hostname                   role    memory      n_cpus    n_gpus
    ----------  -------------------------  -------------------------  ------  --------  --------  --------
             1  k8s-agentpool1-13475325-0  k8s-agentpool1-13475325-0  agent   6.7 Gb           2         0
             2  k8s-agentpool2-13475325-0  k8s-agentpool2-13475325-0  agent   54.93 Gb         6         1
             3  k8s-master-13475325-0      k8s-master-13475325-0      master  6.7 Gb           2         0
    ```

2. Now  we can create a project, you can do that with `Polyaxon Dashboard` or with `polyaxon CLI`

    ```bash
    $ polyaxon project create --name=quick-start --description='Polyaxon quick start.'
    ```

3. Head to your terminal and clone our [quick-start repo](https://github.com/polyaxon/polyaxon-quick-start)

    ```bash
    $ git clone https://github.com/polyaxon/polyaxon-quick-start.git
    ...

    $ cd polyaxon-quick-start
    $ ls

    LICENSE                       polyaxonfile.yml
    README.md                     polyaxonfile_declarations.yml
    model.py                      polyaxonfile_hyperparams.yml
    ```

4. Initialize the project with the same name that you used when you created the project in Polyaxon

    ```bash
    $ polyaxon init quick-start

    Polyaxonfile was created successfully `polyaxonfile.yml`
    ```

5. Let's open the created `polyaxon.yml`, since we cloned the project,
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
         in this case we want to run our code with the specified tensorflow docker image.
         We are also installing the [polyaxon helper](/reference_polyaxon_helper) library to send metrics at the end of the experiment.

6. Now let's upload our code to create a commit on Polyaxon

    ```bash
    $ polyaxon upload
    ```

7. Then start the experiment

    ```bash
    $ polyaxon run

    Experiment was created
    ```

    !!! tip
        You can merge these 2 steps: `polyaxon run -u`

8. Check your project experiments list

    ```bash
    $ polyaxon project experiments
    ```

    sequence | name | user | project | status | created_at
    ---------|------|------|---------|--------|-----------
    1 | root.quick-start.1 | root | root.quick-start| Scheduled | seconds ago


9. Check the experiment logs and resource

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
    master.1                          0.47 Gb / 6.79 Gb    120.47% - 6
    ...
    ```

11. Start another experiment

    ```bash
    $ polyaxon run -f polyaxonfile_declarations.yml
    ```

12. Start an experiment group

    Check the run definition:

    ```bash
    $ polyaxon check -f polyaxonfile_hyperparams.yml -x

    Polyaxonfile valid

    The matrix-space has 20 experiments, with 2 concurrent runs, and random search.
    ```

    Check the matrix definition:

    ```bash
    $ polyaxon check -f polyaxonfile_hyperparams.yml -m

    Polyaxonfile valid

    The matrix definition is:
    {'learning_rate': 0.001, 'activation': 'relu', 'dropout': 0.25}
    {'learning_rate': 0.001, 'activation': 'sigmoid', 'dropout': 0.25}
    {'learning_rate': 0.001, 'activation': 'relu', 'dropout': 0.3}
    {'learning_rate': 0.001, 'activation': 'sigmoid', 'dropout': 0.3}
    ...
    ...
    ```

    ```bash
    $ polyaxon run -f polyaxonfile_declarations.yml

    Creating an experiment group with 20 experiments.

    Experiment group was created
    ```

13. Check experiments in the group

    ```bash
    polyaxon group -g 1 get

    Experiment group info:

    -----------------------  ------------------
    sequence                 1
    unique_name              root.quick-start.1
    user                     root
    project_name             root.quick-start
    created_at               a few seconds ago
    concurrency              2
    num_experiments          20
    num_pending_experiments  18
    num_running_experiments  0
    -----------------------  ------------------
    ```

    ```bash
    $ polyaxon group -g 1 experiments

    Experiments for experiment group `1`.


    Navigation:

    -----  --
    count  20
    -----  --

    Experiments:

      sequence  unique_name            user    last_status    created_at          num_jobs  finished_at    started_at
    ----------  ---------------------  ------  -------------  -----------------  ---------  -------------  -----------------
             4  root.quick-start.1.4   root    Created        a few seconds ago          0
             5  root.quick-start.1.5   root    Created        a few seconds ago          0
             6  root.quick-start.1.6   root    Created        a few seconds ago          0
             7  root.quick-start.1.7   root    Created        a few seconds ago          0
             8  root.quick-start.1.8   root    Created        a few seconds ago          0
             9  root.quick-start.1.9   root    Created        a few seconds ago          0
            10  root.quick-start.1.10  root    Created        a few seconds ago          0
            11  root.quick-start.1.11  root    Created        a few seconds ago          0
            12  root.quick-start.1.12  root    Running        a few seconds ago          1                 a few seconds ago
            13  root.quick-start.1.13  root    Created        a few seconds ago          0
            14  root.quick-start.1.14  root    Created        a few seconds ago          0
            15  root.quick-start.1.15  root    Running        a few seconds ago          1                 a few seconds ago
            16  root.quick-start.1.16  root    Created        a few seconds ago          0
            17  root.quick-start.1.17  root    Created        a few seconds ago          0
            18  root.quick-start.1.18  root    Created        a few seconds ago          0
            19  root.quick-start.1.19  root    Created        a few seconds ago          0
            20  root.quick-start.1.20  root    Created        a few seconds ago          0
            21  root.quick-start.1.21  root    Created        a few seconds ago          0
            22  root.quick-start.1.22  root    Created        a few seconds ago          0
            23  root.quick-start.1.23  root    Created        a few seconds ago          0
    ```

14. More information about the project in the dashboard

    ```bash
    $ polyaxon dashboard

    Dashboard page will now open in your browser. Continue? [Y/n]: y
    ```

    * Landing page:

        ![index](/images/dashboard/index.png)

    * Login page:

        ![login](/images/dashboard/login.png)

    * Projects list:

        ![project](/images/dashboard/projects.png)

    * Project Details

        ![project](/images/dashboard/project.png)

15. Finally, Let start tensorboard to see the model outputs:

     ```bash
     $ polyaxon project start_tensorboard

     Tensorboard is being deployed for project `quick-start`

        It may take some time before you can access the dashboard.

        If you used an ingress, your dashboard will be available at:

            http://52.226.37.54:80/tensorboard/root/quick-start

        Ohterwise you can use kubectl to get the url.
     ```

Congratulations! You've trained your first experiments with Polyaxon. Behind the scene a couple of things have happened:

 * You uploaded your code, and created a git commit for this version of your code
 * You built a docker image with the latest version of your code
 * You ran the image with the specified command in the polyaxonfile
 * You persisted your logs and outputs to your volume claims
 * You created a group of experiments to fine tune hyperparameters

To gain a deeper understanding on how polyaxon can help you iterate faster with your experiments,
please take some time to familiarize yourself with the [experimentation workflow](experimentation/concepts)

# Polyaxon with an introductory example


Let’s look at an example of how you can use Polyaxon for your deep learning experiments.
This example assumes that both Polyaxon is [installed](installation/introduction) and running.
And you are logged in to your Polyaxon account through the [polyaxon-cli](polyaxon_cli/commands)

1. The first step is to create a project, you can do that with the `Polyaxon-dashboard` or with the `polyaxon-cli`

    ```bash
    $ project create --name=mnist --description='Classification of handwritten images.'
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
    $ polyaxon init mnist

    Polyaxonfile was created successfully `polyaxonfile.yml`
    ```

4. Let's open the created `polyaxon.yml` and set the minimum configuration needed to start an experiment:

    ```yaml
    ---
    version: 1

    project:
      name: mnist

    run:
      image: tensorflow/tensorflow:1.4.1-py3
      cmd: python mnsit.py
    ```

    This configuration specifies:

       * The Polyaxon specification `version` we are using.
       * The `project` namespace we want to run the experiment inside.
       * The `run` section to build and execute our code, in this case we want to run our code with this tensorflow specific docker image.

5. Now let's upload our code to create a commit on Polyaxon

    ```bash
    $ polyaxon upload
    ```

6. Then start the experiment

    ```bash
    $ polyaxon run

    Experiment was created
    ```

7. Check your project experiments list

    ```bash
    $ polyaxon project experiments
    ```

    sequence | name | user | project | status | created_at
    ---------|------|------|---------|--------|-----------
    1 | admin.cats-vs-dogs.7 | admin | admin.cats-vs-dogs | Scheduled | seconds ago


8. Finally, check the experiment logs

    ```bash
    $ polyaxon experiment logs 1
    Building --
    INFO:tensorflow:global_step/sec: 1.59552
    INFO:tensorflow:loss = 0.116677, step = 101 (62.679 sec)
    INFO:tensorflow:global_step/sec: 1.47121
    INFO:tensorflow:loss = 0.0842577, step = 201 (67.969 sec)
    ...
    ```

Congratulations! You've trained your first experiment with Polyaxon. Behind the scene a couple of things have happened:

 * You uploaded your code, and created a git commit for this version of your code
 * You built a docker image with the latest version of your code
 * You ran the image with the specified command in the polyaxonfile
 * You persisted your logs and outputs to your volume claims

To gain a deeper understanding on how polyaxon can help you iterate faster with your experiments,
please take some time to familiarize yourself with the [experimentation workflow](experimentation/concepts)

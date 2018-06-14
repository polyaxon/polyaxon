This section assumes that you have already familiarized yourself with the concept of [experiments](experiments).

In order to add structure to your experiments,
Polyaxon creates a couple of paths for every experiment on the volumes provided during the deployment.

For example, all logs related to an experiment are saved on the logs volume, on:

 * Independent experiment: `/[LOGS MOUNT PATH]/username/project_name/experiments/experiment_sequence`
 * Group experiment: `/[LOGS MOUNT PATH]/username/project_name/groups/group_sequence/experiment_sequence`

The logs are anything that user outputs to the console during the training/execution of the code.

Same as logs, the outputs are saved on the outputs volume, on:

 * Independent experiment: `/[OUTPUTS MOUNT PATH]/username/project_name/experiments/experiment_sequence`
 * Group experiment: `/[OUTPUTS MOUNT PATH]/username/project_name/groups/group_sequence/experiment_sequence`

You don't need to figure out this path or hardcode them manually,
Polyaxon will provide an environment variable for the outputs `POLYAXON_OUTPUTS_PATH`
that you can use to export your outputs, artifacts and checkpoints.
You can also use our helper to get this path [get_outputs_path](/reference_polyaxon_helper/#getting-env-variables-defined-by-polyaxon).

## Saving and checkpointing

Most frameworks provide a ways to save your progress as you train your models.
It's up to the user to decide the frequency and number of checkpoints to keep.

### Saving with Tensorflow

Tensorflow provide different ways for saving and resuming a checkpoint. The easiest is to use the [Estimator](https://www.tensorflow.org/get_started/checkpoints) api.
The Estimator takes care of saving checkpoints automatically,
you only need to specify the top-level directory in which the Estimator stores its information,
This is done by assigning a value to the optional `model_dir` argument of any Estimator's constructor.

In the case of Polyaxon you should assign provided path `POLYAXON_OUTPUTS_PATH`, e.g.

```python
classifier = tf.estimator.DNNClassifier(
    feature_columns=my_feature_columns,
    hidden_units=[10, 10],
    n_classes=3,
    model_dir=get_outputs_path())
```

### Saving with Keras

Keras api provides callbacks and in the case of saving checkpointing,
it is the [ModelCheckpoint](https://keras.io/callbacks/#modelcheckpoint) which should be called.

```python
checkpoint = ModelCheckpoint(get_outputs_path(),
                            monitor='val_loss',
                            verbose=0,
                            save_best_only=True,
                            period=1,
                            mode='auto')
```

### Saving with Pytorch

Pytorch provides different approaches to [save models](http://pytorch.org/docs/stable/notes/serialization.html#recommended-approach-for-saving-a-model)

```python
# This is important because it's not automatic
model_path = '{}/checkpoint1.pth'.format(get_outputs_path())
torch.save(the_model.state_dict(), model_path)
```

or

```python
# This is important because it's not automatic
model_path = '{}/checkpoint20.pth'.format(get_outputs_path())
torch.save(the_model, model_path)
```


## Resuming

Polyaxon provides the possibility to resume the training of an already stopped experiment.

In order for to resume an experiment, the experiment should have some checkpoints to resume from.

You can also resume an experiment with an updated environment or some parameters.

### Resuming with Tensorflow

If you used the Estimator api, you don't need to do anything because the Estimator will take care of resuming your training.
Of course you can have tweak your code to resume from a very specific state.

You just need to call:

```bash
$ polyaxon experiment -xp 23 resume
```


### Resuming with Keras

To resume with keras, your code must be able to load model's weights:

```python
...
model.load_weights(model_weights)
...
```

And you need to call:

```bash
$ polyaxon experiment -xp 23 resume
```


### Resuming with Pytorch

Depending on how you saved your model with pytorch, i.e. overriding or creating multiple checkpoints,
you can resume training by using the pytorch load function

```python
the_model = TheModelClass(*args, **kwargs)
model_path = '{}/checkpoint1.pth'.format(get_outputs_path())
the_model.load_state_dict(torch.load(model_path))
```

or

```python
model_path = '{}/checkpoint20.pth'.format(get_outputs_path())
the_model = torch.load(model_path)
```

and you need to call:

```bash
$ polyaxon experiment -xp 23 resume
```

To resume an experiment with latest code:

```bash
$ polyaxon experiment -xp 23 resume -u
```

To override the config of the experiment you wish to resume, you need to create a polyaxonfile with the override section/params:

```bash
$ polyaxon experiment -xp 23 resume -f polyaxonfile_override.yml
```

When you resume an experiment the outputs of the resuming experiment is added to the outputs of the original experiments.


## Restarting

Sometimes you don't want to resume an experiment, and you wish to keep it and restart training with the same or different code or parameters.
Polyaxon provides a way to do that:

```bash
$ polyaxon experiment -xp 23 restart
```

To restart an experiment with latest code:

```bash
$ polyaxon experiment -xp 23 restart -u
```

To override the config of the experiment you wish to restart, you need to create a polyaxonfile with the override section/params:

```bash
$ polyaxon experiment -xp 23 restart -f polyaxonfile_override.yml
```

For example you can restart an experiment with gpu or with a different learning rate.


## Copying

Another option that Polyaxon offers is to copy an experiment before restarting it.
This option is useful if the user wants to resume the training of an experiment with multiple updated versions of her code or parameters,
what it does is basically it copies all outputs from the experiment to the new experiments.


```bash
$ polyaxon experiment -xp 23 restart --copy
```

To copy an experiment with latest code:

```bash
$ polyaxon experiment -xp 23 restart --copy -u
```

To override the config of the experiment you wish to copy, you need to create a polyaxonfile with the override section/params:

```bash
$ polyaxon experiment -xp 23 --copy restart -f polyaxonfile_override.yml
```

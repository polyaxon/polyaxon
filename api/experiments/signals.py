from experiments.tasks import start_experiment


def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if created and instance.is_independent:
        # Schedule the new experiment to be picked by the spawner
        start_experiment.delay(experiment_id=instance.id)

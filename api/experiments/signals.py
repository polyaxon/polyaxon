from polyaxon_k8s.constants import JobLifeCycle

from experiments.constants import ExperimentLifeCycle


def new_experiment(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if created:
        from experiments.task_status import RedisExperimentStatus
        from experiments.tasks import start_experiment

        RedisExperimentStatus.set_status(instance.id, ExperimentLifeCycle.CREATED)
        if instance.is_independent:
            # Schedule the new experiment to be picked by the spawner
            start_experiment.delay(experiment_id=instance.id)


def new_experiment_job(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs.get('created', False)

    # Check if the experiment is newly created and that we can start it independently
    if created:
        from experiments.task_status import RedisExperimentJobStatus

        RedisExperimentJobStatus.set_status(instance.id, JobLifeCycle.CREATED)
        RedisExperimentJobStatus.monitor(instance.id)

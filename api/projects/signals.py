from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import ExperimentGroup
from projects.tasks import start_group_experiments
from experiments.models import Experiment


@receiver(post_save, sender=ExperimentGroup, dispatch_uid="experiment_group_saved")
def new_experiment_group(sender, **kwargs):

    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Parse polyaxonfile content and create the experiments
    specification = instance.specification
    for xp in range(specification.matrix_space):

        Experiment.objects.create(project=instance.project,
                                  user=instance.user,
                                  experiment_group=instance,
                                  config=specification.parsed_data[xp])

    start_group_experiments.delay(instance.id)

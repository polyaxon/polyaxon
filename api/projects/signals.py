from django.db.models.signals import post_save
from django.dispatch import receiver

from clusters.models import Cluster
from projects.models import PolyaxonSpec
from projects.tasks import start_group_experiments
from experiments.models import Experiment


@receiver(post_save, sender=PolyaxonSpec, dispatch_uid="spec_saved")
def new_spec(sender, **kwargs):
    """"""

    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if not created:
        return

    # Parse polyaxonfile content and create the experiments
    specification = instance.specification
    for xp in range(specification.matrix_space):

        cluster = None
        if specification.settings and specification.settings.cluster_uuid:
            cluster = Cluster.objects.filter(uuid=specification.settings.cluster_uuid).first()
        if not cluster:
            # TODO: add logging: using default cluster
            cluster = Cluster.objects.filter(user=instance.user).last()
        Experiment.objects.create(cluster=cluster,
                                  project=instance.project,
                                  user=instance.user,
                                  spec=instance,
                                  config=specification.parsed_data[xp])

    start_group_experiments.delay(instance.id)

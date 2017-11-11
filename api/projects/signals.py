from clusters.models import Cluster
from projects.tasks import start_group_experiments


def new_spec(sender, **kwargs):
    from experiments.models import Experiment

    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if created:
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
                                      config=specification.get_parsed_data_at(xp))

        start_group_experiments.delay(instance.id)

from clusters.models import Cluster
from projects.tasks import start_group_experiments


def new_spec(sender, **kwargs):
    from experiments.models import Experiment

    instance = kwargs['instance']
    created = kwargs.get('created', False)

    if created:
        # Parse polyaxonfile content and create the experiments
        for xp in range(instance.parsed_content.matrix_space):
            content = instance.parsed_content.get_validated_data_at(xp)
            cluster = None
            if content.cluster_id:
                cluster = Cluster.objects.filter(id=content.cluster_id).first()
            if not cluster:
                # TODO: add logging: using default cluster
                cluster = Cluster.objects.filter(user=instance.user).last()
            Experiment.objects.create(cluster=cluster,
                                      project=instance.project,
                                      user=instance.user,
                                      spec=instance,
                                      config=content)

        start_group_experiments.delay(instance.id)

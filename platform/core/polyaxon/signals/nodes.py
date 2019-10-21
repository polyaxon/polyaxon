from hestia.signal_decorators import ignore_raw, ignore_updates

from django.db.models.signals import post_save
from django.dispatch import receiver

import auditor

from db.models.nodes import NodeGPU
from events.registry.cluster import CLUSTER_NODE_GPU


@receiver(post_save, sender=NodeGPU, dispatch_uid="node_gpu_created")
@ignore_updates
@ignore_raw
def node_gpu_created(sender, **kwargs):
    instance = kwargs['instance']
    auditor.record(event_type=CLUSTER_NODE_GPU,
                   instance=instance)

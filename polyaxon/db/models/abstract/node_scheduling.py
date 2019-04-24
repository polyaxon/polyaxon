from django.db import models


class NodeSchedulingModel(models.Model):
    node_scheduled = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        abstract = True

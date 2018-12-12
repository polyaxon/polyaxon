from django.db import models


class LiveManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(deleted=False)

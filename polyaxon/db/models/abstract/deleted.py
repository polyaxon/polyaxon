from django.db import models

from db.managers.deleted import ArchivedManager, LiveManager
from django.db import models

from db.managers.deleted import ArchivedManager, LiveManager


class DeletedModel(models.Model):
    deleted = models.BooleanField(default=False)

    objects = LiveManager()
    all = models.Manager()
    archived = ArchivedManager()

    class Meta:
        abstract = True

    def archive(self) -> bool:
        if self.deleted:
            return False

        self.deleted = True
        self.save(update_fields=['deleted'])
        return True

    def restore(self) -> bool:
        if not self.deleted:
            return False

        self.deleted = False
        self.save(update_fields=['deleted'])
        return True

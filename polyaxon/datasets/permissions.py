import logging

from rest_framework import permissions

from datasets.models import Dataset

logger = logging.getLogger("polyaxon.datasets.permissions")


def has_dataset_permissions(user, dataset, request_method):
    """This logic is extracted here to be used also with Sanic api."""
    # Superusers and the creator is allowed to do everything
    if user.is_staff or dataset.user == user:
        return True

    # Other user
    return request_method in permissions.SAFE_METHODS and dataset.is_public


class IsDatasetOwnerOrPublicReadOnly(permissions.BasePermission):
    """Custom permission to only allow owner to update/delete dataset.

    Other users can have read access if the project is public."""

    def has_object_permission(self, request, view, obj):
        # Check object type
        if not isinstance(obj, Dataset):
            logger.warning('Trying to check datasets permission against {}'.format(
                obj.__class__.__name__))
            return False

        return has_dataset_permissions(user=request.user,
                                       dataset=obj,
                                       request_method=request.method)

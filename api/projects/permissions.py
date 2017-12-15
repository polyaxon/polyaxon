# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from projects.models import Project

logger = logging.getLogger("polyaxon.projects.permissions")


class IsProjectOwnerOrPublicReadOnly(permissions.BasePermission):
    """Custom permission to only allow owner to update/delete project.

    Other users can have read access if the project is public."""

    def has_object_permission(self, request, view, obj):
        # Check object type
        if not isinstance(obj, Project):
            logger.warning('Trying to check projects permission again {}'.format(
                obj.__class__.__name__))
            return False

        # The creator is allowed to do everything
        if obj.user == request.user:
            return True

        # Other user
        return request.method in permissions.SAFE_METHODS and obj.is_public


class IsItemProjectOwnerOrPublicReadOnly(permissions.BasePermission):
    """Custom permission to only allow owner of project to update/delete project items.

    Other users can have read access if the project is public."""

    def has_object_permission(self, request, view, obj):
        # Check that obj has project attr
        if not hasattr(obj, 'project'):
            logger.warning('Trying to check project item permission again {}'.format(
                obj.__class__.__name__))
            return False

        # The creator is allowed to do everything
        if obj.project.user == request.user:
            return True

        # Other user
        return request.method in permissions.SAFE_METHODS and obj.project.is_public


def check_access_project_item(view, request, project):
    permission = IsProjectOwnerOrPublicReadOnly()
    if not permission.has_object_permission(request, view, project):
        view.permission_denied(
            request, message=getattr(permission, 'message', None)
        )


def get_permissible_project(view):
    username = view.kwargs['username']
    project_name = view.kwargs['name']
    project = get_object_or_404(Project, name=project_name, user__username=username)

    # Check project permissions
    check_access_project_item(view=view, request=view.request, project=project)

    return project

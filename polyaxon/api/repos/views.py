import logging
import os

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.http import Http404, HttpResponseServerError

import auditor
import ci
import conf

from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    PostEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.project import ProjectResourceListEndpoint
from api.repos.serializers import ExternalRepoSerializer, RepoSerializer
from api.repos.tasks import handle_new_files
from api.utils.views.protected import ProtectedView
from api.utils.views.upload import UploadView
from db.models.repos import ExternalRepo, Repo
from event_manager.events.repo import REPO_CREATED, REPO_DOWNLOADED
from libs.archive import archive_repo
from libs.repos import git
from libs.repos.git import GitCloneException
from scopes.authentication.internal import InternalAuthentication, is_authenticated_internal_user
from scopes.permissions.internal import IsAuthenticatedOrInternal

_logger = logging.getLogger('polyaxon.views.repos')


class RepoDetailView(ProjectResourceListEndpoint,
                     RetrieveEndpoint,
                     UpdateEndpoint,
                     DestroyEndpoint):
    """
    get:
        Get a repo details.
    patch:
        Update a repo details.
    delete:
        Delete a repo.
    """
    def get_queryset(self):
        if self.project.has_external_repo:
            return ExternalRepo.objects
        return Repo.objects

    def get_serializer_class(self):
        if self.project.has_external_repo:
            return ExternalRepoSerializer
        return RepoSerializer

    def get_object(self):
        if self._object:
            return self._object
        if self.project.has_external_repo:
            self._object = get_object_or_404(ExternalRepo, project=self.project)
        else:
            self._object = get_object_or_404(Repo, project=self.project)
        return self._object


class RepoDownloadView(ProjectResourceListEndpoint, ProtectedView):
    """Download repo code as tar.gz."""
    HANDLE_UNAUTHENTICATED = False
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrInternal,)

    def get_object(self):
        if self._object:
            return self._object
        if self.project.has_repo:
            self._object = get_object_or_404(Repo, project=self.project)
        elif self.project.has_external_repo:
            self._object = get_object_or_404(ExternalRepo, project=self.project)
        else:
            raise Http404('Repo was not found')
        if not is_authenticated_internal_user(self.request.user):
            auditor.record(event_type=REPO_DOWNLOADED,
                           instance=self._object,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           external=False)
        return self._object

    def get(self, request, *args, **kwargs):
        repo = self.get_object()
        commit = self.request.query_params.get('commit', None)
        archived_path, archive_name = archive_repo(repo_git=repo.git,
                                                   repo_name=self.project.name,
                                                   commit=commit)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))


class ExternalRepoSetView(ProjectResourceListEndpoint, CreateEndpoint):
    queryset = ExternalRepo.objects
    serializer_class = ExternalRepoSerializer

    def perform_create(self, serializer):
        try:
            repo = serializer.save(project=self.project)
            auditor.record(event_type=REPO_CREATED,
                           instance=repo,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           external=True)
        except GitCloneException as e:
            raise ValidationError(e)

    def create(self, request, *args, **kwargs):
        if self.project.has_repo:
            self.permission_denied(
                self.request,
                'The Project `{}` is currently using an internal repo '
                'as main code tracker.'.format(
                    self.project.name))

        try:
            repo = ExternalRepo.objects.get(project=self.project)
        except ExternalRepo.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer=serializer)
            return Response(status=status.HTTP_201_CREATED)
        if not os.path.isdir(repo.project_path):
            git.external.set_git_repo(repo)
        elif repo.git_url != request.data.get('git_url'):
            raise ValidationError(
                'Project was already initialized with a different git url: {}'.format(
                    request.data.get('git_url')
                ))
        return Response(status=status.HTTP_200_OK)


class ExternalRepoSyncView(ProjectResourceListEndpoint, PostEndpoint):
    queryset = ExternalRepo.objects
    serializer_class = ExternalRepoSerializer

    def get_object(self):
        if self._object:
            return self._object
        self._object = get_object_or_404(ExternalRepo, project=self.project)
        return self._object

    def post(self, request, *args, **kwargs):
        repo = self.get_object()
        if not os.path.isdir(repo.project_path):
            git.external.set_git_repo(repo)

        if ci.trigger(project=self.project):
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_200_OK,
                        data='Could not trigger the project CI.')


class RepoUploadView(ProjectResourceListEndpoint, UploadView):
    """Upload code to a repo."""

    def get_object(self):
        if self.project.has_external_repo:
            self.permission_denied(
                self.request,
                'The Project `{}` is currently using an external_repo '
                'as main code tracker.'.format(
                    self.project.name))

        if conf.get('MOUNT_CODE_IN_NOTEBOOKS') and self.project.has_notebook:
            self.permission_denied(
                self.request,
                'The Project `{}` is currently running a Notebook. '
                'You must stop it before uploading a new version of the code.'.format(
                    self.project.name))

        repo, created = Repo.objects.get_or_create(project=self.project)
        if not created and not os.path.isdir(repo.project_path):
            git.internal.set_git_repo(repo)
        else:
            auditor.record(event_type=REPO_CREATED,
                           instance=repo,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           external=False)
        return repo

    def put(self, request, *args, **kwargs):
        user = request.user
        repo = self.get_object()
        path = os.path.join(conf.get('UPLOAD_MOUNT_PATH'), user.username)
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            tar_file_name = self._handle_posted_data(request=request,
                                                     filename='{}.tar.gz'.format(repo.project.name),
                                                     directory=path,
                                                     upload_filename='repo')
        except (IOError, os.error) as e:  # pragma: no cover
            _logger.warning(
                'IOError while trying to save posted data (%s): %s', e.errno, e.strerror)
            return HttpResponseServerError()

        json_data = self._handle_json_data(request)
        delay = json_data.get('delay', False)
        sync = json_data.get('sync', False)

        if delay is False:
            file_handler = handle_new_files
        else:
            file_handler = handle_new_files.delay

        file_handler(user_id=user.id, repo_id=repo.id, tar_file_name=tar_file_name)

        if sync:
            if ci.trigger(project=self.project):
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_200_OK,
                            data='Could not trigger the project CI.')

        # do some stuff with uploaded file
        return Response(status=status.HTTP_200_OK)

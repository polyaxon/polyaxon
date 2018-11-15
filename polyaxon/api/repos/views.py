import logging
import os

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.conf import settings
from django.http import HttpResponseServerError

import auditor

from api.endpoint.base import DestroyEndpoint, RetrieveEndpoint, UpdateEndpoint
from api.endpoint.project import ProjectResourceListEndpoint
from api.repos.serializers import RepoSerializer
from api.repos.tasks import handle_new_files
from api.utils.views.protected import ProtectedView
from api.utils.views.upload import UploadView
from db.models.repos import Repo
from event_manager.events.repo import REPO_CREATED, REPO_DOWNLOADED
from libs.archive import archive_repo
from libs.repos.git import set_git_repo
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
    queryset = Repo.objects
    serializer_class = RepoSerializer

    def get_object(self):
        return get_object_or_404(Repo, project=self.project)


class DownloadFilesView(ProjectResourceListEndpoint, ProtectedView):
    """Download repo code as tar.gz."""
    HANDLE_UNAUTHENTICATED = False
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrInternal, )

    def get_object(self):
        repo = get_object_or_404(Repo, project=self.project)
        if not is_authenticated_internal_user(self.request.user):
            auditor.record(event_type=REPO_DOWNLOADED,
                           instance=repo,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return repo

    def get(self, request, *args, **kwargs):
        repo = self.get_object()
        commit = self.request.query_params.get('commit', None)
        archived_path, archive_name = archive_repo(repo_git=repo.git,
                                                   repo_name=self.project.name,
                                                   commit=commit)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))


class UploadFilesView(ProjectResourceListEndpoint, UploadView):
    """Upload code to a repo."""

    def get_object(self):
        if self.project.has_notebook:
            self.permission_denied(
                self.request,
                'The Project `{}` is currently running a Notebook. '
                'You must stop it before uploading a new version of the code.'.format(
                    self.project.name))
        repo, created = Repo.objects.get_or_create(project=self.project)
        if not created and not os.path.isdir(repo.project_path):
            set_git_repo(repo)
        else:
            auditor.record(event_type=REPO_CREATED,
                           instance=repo,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return repo

    def put(self, request, *args, **kwargs):
        user = request.user
        repo = self.get_object()
        path = os.path.join(settings.UPLOAD_MOUNT_PATH, user.username)
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
        is_async = json_data.get('async', False)

        if is_async is False:
            file_handler = handle_new_files
        else:
            file_handler = handle_new_files.delay

        file_handler(user_id=user.id, repo_id=repo.id, tar_file_name=tar_file_name)

        # do some stuff with uploaded file
        return Response(status=200)

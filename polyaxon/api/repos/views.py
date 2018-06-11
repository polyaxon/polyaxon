import logging
import os

from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.conf import settings
from django.http import Http404, HttpResponseServerError

import auditor

from api.repos.serializers import RepoSerializer
from api.repos.tasks import handle_new_files
from api.utils.views import ProtectedView, UploadView
from db.models.repos import Repo
from event_manager.events.repo import REPO_CREATED, REPO_DOWNLOADED
from libs.permissions.authentication import InternalAuthentication, is_internal_user
from libs.permissions.internal import IsAuthenticatedOrInternal
from libs.permissions.projects import get_permissible_project
from libs.repos import git
from libs.repos.git import set_git_repo

_logger = logging.getLogger('polyaxon.views.repos')


class RepoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(Repo, project=get_permissible_project(view=self))


class DownloadFilesView(ProtectedView):
    HANDLE_UNAUTHENTICATED = False
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrInternal, )

    def get_object(self):
        project = get_permissible_project(view=self)
        try:
            repo = Repo.objects.get(project=project)
        except Repo.DoesNotExist:
            raise Http404('Repo does not exist.')
        if not is_internal_user(self.request.user):
            auditor.record(event_type=REPO_DOWNLOADED, instance=repo, actor_id=self.request.user.id)
        return repo

    def get(self, request, *args, **kwargs):
        repo = self.get_object()
        archived_path, archive_name = git.archive_repo(repo.git, repo.project.name)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))


class UploadFilesView(UploadView):

    def get_object(self):
        project = get_permissible_project(view=self)
        if project.has_notebook:
            self.permission_denied(
                self.request,
                'The Project `{}` is currently running a Notebook. '
                'You must stop it before uploading a new version of the code.'.format(project.name))
        repo, created = Repo.objects.get_or_create(project=project)
        if not created and not os.path.isdir(repo.user_path):
            set_git_repo(repo)
        else:
            auditor.record(event_type=REPO_CREATED, instance=repo, actor_id=self.request.user.id)
        return repo

    def put(self, request, *args, **kwargs):
        user = request.user
        repo = self.get_object()
        path = os.path.join(settings.UPLOAD_ROOT, user.username)
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
        is_async = json_data.get('async')

        if is_async is False:
            file_handler = handle_new_files
        else:
            file_handler = handle_new_files.delay

        file_handler(user_id=user.id, repo_id=repo.id, tar_file_name=tar_file_name)

        # do some stuff with uploaded file
        return Response(status=204)

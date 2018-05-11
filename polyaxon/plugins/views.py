from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404

import auditor

from event_manager.events.notebook import (
    NOTEBOOK_STARTED_TRIGGERED,
    NOTEBOOK_STOPPED_TRIGGERED,
    NOTEBOOK_VIEWED
)
from event_manager.events.tensorboard import (
    TENSORBOARD_STARTED_TRIGGERED,
    TENSORBOARD_STOPPED_TRIGGERED,
    TENSORBOARD_VIEWED
)
from experiments.statuses import ExperimentLifeCycle
from libs.utils import to_bool
from libs.views import ProtectedView
from plugins.serializers import NotebookJobSerializer, TensorboardJobSerializer
from plugins.tasks import build_notebook, start_tensorboard, stop_notebook, stop_tensorboard
from projects.models import Project
from projects.permissions import IsProjectOwnerOrPublicReadOnly, get_permissible_project
from repos import git
from runner.schedulers import notebook_scheduler, tensorboard_scheduler


class StartTensorboardView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = TensorboardJobSerializer
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    @staticmethod
    def _get_default_tensorboard_config():
        return {
            'config': {
                'version': 1,
                'kind': 'plugin',
                'run': {'image': settings.TENSORBOARD_DOCKER_IMAGE}
            }
        }

    def _create_tensorboard(self, project):
        config = self.request.data or self._get_default_tensorboard_config()
        serializer = self.get_serializer(instance=project.tensorboard, data=config)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user, project=project)
        auditor.record(event_type=TENSORBOARD_STARTED_TRIGGERED,
                       instance=instance,
                       target='project',
                       actor_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.has_tensorboard:
            return Response(data='Tensorboard is already running', status=status.HTTP_200_OK)
        self._create_tensorboard(obj)
        if not obj.tensorboard.is_running:
            start_tensorboard.delay(project_id=obj.id)
        return Response(status=status.HTTP_201_CREATED)


class StopTensorboardView(CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.has_tensorboard:
            stop_tensorboard.delay(project_id=obj.id)
            auditor.record(event_type=TENSORBOARD_STOPPED_TRIGGERED,
                           instance=obj.tensorboard,
                           target='project',
                           actor_id=self.request.user.id)
        return Response(status=status.HTTP_200_OK)


class StartNotebookView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = NotebookJobSerializer
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    def _create_notebook(self, project):
        serializer = self.get_serializer(instance=project.notebook, data=self.request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user, project=project)
        auditor.record(event_type=NOTEBOOK_STARTED_TRIGGERED,
                       instance=instance,
                       target='project',
                       actor_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.has_notebook:
            return Response(data='Notebook is already running', status=status.HTTP_200_OK)
        self._create_notebook(obj)
        if not obj.notebook.is_running:
            build_notebook.delay(project_id=obj.id)
        return Response(status=status.HTTP_201_CREATED)


class StopNotebookView(CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.has_notebook:
            commit = request.data.get('commit')
            commit = to_bool(commit) if commit is not None else True
            if commit:
                # Commit changes
                git.commit(obj.repo.path, request.user.email, request.user.username)
            else:
                # Reset changes
                git.undo(obj.repo.path)
            stop_notebook.delay(project_id=obj.id)
            auditor.record(event_type=NOTEBOOK_STOPPED_TRIGGERED,
                           instance=obj.notebook,
                           target='project',
                           actor_id=self.request.user.id)
        elif obj.notebook and obj.notebook.is_running:
            obj.notebook.set_status(status=ExperimentLifeCycle.STOPPED,
                                    message='Notebook was stopped')
        return Response(status=status.HTTP_200_OK)


class PluginJobView(ProtectedView):
    def audit(self, project):
        pass

    @staticmethod
    def get_base_path(project):
        return ''

    @staticmethod
    def get_base_params(project):
        return ''

    def has_plugin_job(self, project):
        raise NotImplementedError

    def get_service_url(self, project):
        raise NotImplementedError

    def get_object(self):
        return get_permissible_project(view=self)

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        if not self.has_plugin_job(project):
            raise Http404
        self.audit(project=project)
        service_url = self.get_service_url(project=project)
        path = '/{}'.format(service_url.strip('/'))
        base_path = self.get_base_path(project)
        base_params = self.get_base_params(project)
        if self.kwargs['path']:
            path = '{}/{}'.format(path, self.kwargs['path'].strip('/'))
        elif base_path:
            path = '{}/{}'.format(path, base_path)
        if request.GET:
            path = '{}?{}'.format(path, request.GET.urlencode())
            if base_params:
                path = '{}&{}'.format(path, base_params)
        elif base_params:
            path = '{}?{}'.format(path, base_params)
        else:
            path = path + '/'
        return self.redirect(path=path)


class NotebookView(PluginJobView):
    @staticmethod
    def get_base_path(project):
        return 'tree'

    @staticmethod
    def get_base_params(project):
        return 'token={}'.format(notebook_scheduler.get_notebook_token(project=project))

    def get_service_url(self, project):
        return notebook_scheduler.get_notebook_url(project=project)

    def has_plugin_job(self, project):
        return project.has_notebook

    def audit(self, project):
        auditor.record(event_type=NOTEBOOK_VIEWED,
                       instance=project.notebook,
                       target='project',
                       actor_id=self.request.user.id)


class TensorboardView(PluginJobView):
    def get_service_url(self, project):
        return tensorboard_scheduler.get_tensorboard_url(project=project)

    def has_plugin_job(self, project):
        return project.has_tensorboard

    def audit(self, project):
        auditor.record(event_type=TENSORBOARD_VIEWED,
                       instance=project.tensorboard,
                       target='project',
                       actor_id=self.request.user.id)

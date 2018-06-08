from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404

import auditor

from api.plugins.serializers import NotebookJobSerializer, TensorboardJobSerializer
from api.utils.views import ProtectedView
from constants.experiments import ExperimentLifeCycle
from db.models.projects import Project
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
from libs.permissions.projects import IsProjectOwnerOrPublicReadOnly, get_permissible_project
from libs.repos import git
from libs.utils import to_bool
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks
from polyaxon_schemas.polyaxonfile.specification import TensorboardSpecification


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
        specification = TensorboardSpecification.create_specification(
            {'image': settings.TENSORBOARD_DOCKER_IMAGE})
        return {'config': specification}

    def _create_tensorboard(self, project):
        config = self.request.data or self._get_default_tensorboard_config()
        serializer = self.get_serializer(data=config)
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
            celery_app.send_task(
                SchedulerCeleryTasks.TENSORBOARDS_START,
                kwargs={'tensorboard_job_id': obj.tensorboard.id},
                countdown=1)
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
            celery_app.send_task(
                SchedulerCeleryTasks.TENSORBOARDS_STOP,
                kwargs={'tensorboard_job_id': obj.tensorboard.id})
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
        serializer = self.get_serializer(data=self.request.data)
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
        notebook = obj.notebook
        if not notebook.is_running:
            celery_app.send_task(
                SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD,
                kwargs={'notebook_job_id': notebook.id},
                countdown=1)
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
            celery_app.send_task(
                SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
                kwargs={'notebook_job_id': obj.notebook.id})
            auditor.record(event_type=NOTEBOOK_STOPPED_TRIGGERED,
                           instance=obj.notebook,
                           target='project',
                           actor_id=self.request.user.id,
                           countdown=1)
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
        from scheduler import notebook_scheduler

        return 'token={}'.format(notebook_scheduler.get_notebook_token(notebook=project.notebook))

    def get_service_url(self, project):
        from scheduler import notebook_scheduler

        return notebook_scheduler.get_notebook_url(notebook=project.notebook)

    def has_plugin_job(self, project):
        return project.has_notebook

    def audit(self, project):
        auditor.record(event_type=NOTEBOOK_VIEWED,
                       instance=project.notebook,
                       target='project',
                       actor_id=self.request.user.id)


class TensorboardView(PluginJobView):
    def get_service_url(self, project):
        from scheduler import tensorboard_scheduler

        return tensorboard_scheduler.get_tensorboard_url(tensorboard=project.tensorboard)

    def has_plugin_job(self, project):
        return project.has_tensorboard

    def audit(self, project):
        auditor.record(event_type=TENSORBOARD_VIEWED,
                       instance=project.tensorboard,
                       target='project',
                       actor_id=self.request.user.id)

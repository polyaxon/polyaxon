from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from django.http import Http404

import auditor

from api.filters import OrderingFilter, QueryFilter
from api.plugins.serializers import (
    NotebookJobSerializer,
    ProjectTensorboardJobSerializer,
    TensorboardJobSerializer
)
from api.utils.views import PostAPIView, ProtectedView
from constants.experiments import ExperimentLifeCycle
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.projects import Project
from db.models.tensorboards import TensorboardJob
from event_manager.events.notebook import (
    NOTEBOOK_STARTED_TRIGGERED,
    NOTEBOOK_STOPPED_TRIGGERED,
    NOTEBOOK_VIEWED
)
from event_manager.events.project import PROJECT_TENSORBOARDS_VIEWED
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
    """Start a tensorboard."""
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

    def _create_tensorboard(self, project, experiment_group=None, experiment=None):
        config = self.request.data or self._get_default_tensorboard_config()
        serializer = self.get_serializer(data=config)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user,
                                   project=project,
                                   experiment_group=experiment_group,
                                   experiment=experiment)
        auditor.record(event_type=TENSORBOARD_STARTED_TRIGGERED,
                       instance=instance,
                       target='project',
                       actor_id=self.request.user.id)

    def _handle_project_tensorboard(self, project):
        if project.has_tensorboard:
            return None
        self._create_tensorboard(project=project)
        return project.tensorboard

    def _handle_group_tensorboard(self, project, group):
        if group.has_tensorboard:
            return None
        self._create_tensorboard(project=project, experiment_group=group)
        return group.tensorboard

    def _handle_experiment_tensorboard(self, project, experiment):
        if experiment.has_tensorboard:
            return None
        self._create_tensorboard(project=project, experiment=experiment)
        return experiment.tensorboard

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')
        if experiment_id:
            experiment = get_object_or_404(Experiment, project=project, id=experiment_id)
            tensorboard = self._handle_experiment_tensorboard(project=project,
                                                              experiment=experiment)
        elif group_id:
            group = get_object_or_404(ExperimentGroup, project=project, id=group_id)
            tensorboard = self._handle_group_tensorboard(project=project, group=group)
        else:
            tensorboard = self._handle_project_tensorboard(project=project)

        if not tensorboard:
            return Response(data='Tensorboard is already running', status=status.HTTP_200_OK)

        if not tensorboard.is_running:
            celery_app.send_task(
                SchedulerCeleryTasks.TENSORBOARDS_START,
                kwargs={'tensorboard_job_id': tensorboard.id},
                countdown=1)
        return Response(status=status.HTTP_201_CREATED)


class StopTensorboardView(PostAPIView):
    """Stop a tensorboard."""
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated, IsProjectOwnerOrPublicReadOnly)
    lookup_field = 'name'

    def filter_queryset(self, queryset):
        username = self.kwargs['username']
        return queryset.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')

        if experiment_id:
            experiment = get_object_or_404(Experiment, project=project, id=experiment_id)
            has_tensorboard = experiment.has_tensorboard
            tensorboard = experiment.tensorboard
        elif group_id:
            group = get_object_or_404(ExperimentGroup, project=project, id=group_id)
            has_tensorboard = group.has_tensorboard
            tensorboard = group.tensorboard
        else:
            has_tensorboard = project.has_tensorboard
            tensorboard = project.tensorboard

        if has_tensorboard:
            celery_app.send_task(
                SchedulerCeleryTasks.TENSORBOARDS_STOP,
                kwargs={
                    'project_name': project.unique_name,
                    'project_uuid': project.uuid.hex,
                    'tensorboard_job_name': tensorboard.unique_name,
                    'tensorboard_job_uuid': tensorboard.uuid.hex,
                    'update_status': True
                })
            auditor.record(event_type=TENSORBOARD_STOPPED_TRIGGERED,
                           instance=tensorboard,
                           target='project',
                           actor_id=self.request.user.id)
        return Response(status=status.HTTP_200_OK)


class StartNotebookView(CreateAPIView):
    """Start a notebook."""
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


class StopNotebookView(PostAPIView):
    """Stop a tensorboard."""
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
                kwargs={
                    'project_name': obj.unique_name,
                    'project_uuid': obj.uuid.hex,
                    'notebook_job_name': obj.notebook.unique_name,
                    'notebook_job_uuid': obj.notebook.uuid.hex,
                    'update_status': True
                })
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
    def audit(self, instance):
        pass

    @staticmethod
    def get_base_path(instance):
        return ''

    @staticmethod
    def get_base_params(instance):
        return ''

    def has_plugin_job(self, instance):
        raise NotImplementedError

    def get_service_url(self, instance):
        raise NotImplementedError

    def get_object(self):
        return get_permissible_project(view=self)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.has_plugin_job(instance):
            raise Http404
        self.audit(instance=instance)
        service_url = self.get_service_url(instance=instance)
        path = '/{}'.format(service_url.strip('/'))
        base_path = self.get_base_path(instance)
        base_params = self.get_base_params(instance)
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
    def get_base_path(instance):
        return 'tree'

    @staticmethod
    def get_base_params(instance):
        from scheduler import notebook_scheduler

        return 'token={}'.format(notebook_scheduler.get_notebook_token(notebook=instance.notebook))

    def get_service_url(self, instance):
        from scheduler import notebook_scheduler

        return notebook_scheduler.get_notebook_url(notebook=instance.notebook)

    def has_plugin_job(self, instance):
        return instance.has_notebook

    def audit(self, instance):
        auditor.record(event_type=NOTEBOOK_VIEWED,
                       instance=instance.notebook,
                       target='project',
                       actor_id=self.request.user.id)


class TensorboardView(PluginJobView):
    def get_object(self):
        project = get_permissible_project(view=self)
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')

        if experiment_id:
            return get_object_or_404(Experiment, project=project, id=experiment_id)
        elif group_id:
            return get_object_or_404(ExperimentGroup, project=project, id=group_id)

        return project

    def get_service_url(self, instance):
        from scheduler import tensorboard_scheduler

        return tensorboard_scheduler.get_tensorboard_url(tensorboard=instance.tensorboard)

    def has_plugin_job(self, instance):
        return instance.has_tensorboard

    def audit(self, instance):
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')
        if experiment_id:
            target = 'experiment'
        elif group_id:
            target = 'experiment_group'
        else:
            target = 'project'
        auditor.record(event_type=TENSORBOARD_VIEWED,
                       instance=instance.tensorboard,
                       target=target,
                       actor_id=self.request.user.id)


class ProjectTensorboardListView(ListAPIView):
    """List an tensorboards under a project."""
    queryset = TensorboardJob.objects.all()
    serializer_class = ProjectTensorboardJobSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'tensorboard'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        project = get_permissible_project(view=self)
        auditor.record(event_type=PROJECT_TENSORBOARDS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id)
        queryset = queryset.filter(project=project)
        return super().filter_queryset(queryset=queryset)

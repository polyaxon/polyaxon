from hestia.bool_utils import to_bool
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from django.http import Http404

import auditor
import conf

from api.endpoint.base import CreateEndpoint, ListEndpoint, PostEndpoint
from api.endpoint.project import ProjectEndpoint, ProjectResourceListEndpoint
from api.filters import OrderingFilter, QueryFilter
from api.plugins.serializers import (
    NotebookJobSerializer,
    ProjectTensorboardJobSerializer,
    TensorboardJobSerializer
)
from api.utils.views.protected import ProtectedView
from constants.experiments import ExperimentLifeCycle
from constants.jobs import JobLifeCycle
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import Experiment
from db.models.tensorboards import TensorboardJob
from db.models.tokens import Token
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
from libs.repos import git
from polyaxon.celery_api import celery_app
from polyaxon.settings import SchedulerCeleryTasks
from schemas.notebook_backend import NotebookBackend
from schemas.specifications import NotebookSpecification, TensorboardSpecification
from scopes.authentication.internal import InternalAuthentication
from scopes.permissions.internal import IsInitializer


class StartTensorboardView(ProjectEndpoint, CreateEndpoint):
    """Start a tensorboard."""
    serializer_class = TensorboardJobSerializer

    @staticmethod
    def _get_default_tensorboard_config():
        specification = TensorboardSpecification.create_specification(
            {'image': conf.get('TENSORBOARD_DOCKER_IMAGE')})
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
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)

    def _handle_project_tensorboard(self, project):
        if project.has_tensorboard:
            return None
        self._create_tensorboard(project=project)
        project.clear_cached_properties()
        return project.tensorboard

    def _handle_group_tensorboard(self, project, group):
        if group.has_tensorboard:
            return None
        self._create_tensorboard(project=project, experiment_group=group)
        group.clear_cached_properties()
        return group.tensorboard

    def _handle_experiment_tensorboard(self, project, experiment):
        if experiment.has_tensorboard:
            return None
        self._create_tensorboard(project=project, experiment=experiment)
        experiment.clear_cached_properties()
        return experiment.tensorboard

    def post(self, request, *args, **kwargs):
        project = self.project
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
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_201_CREATED)


class StopTensorboardView(ProjectEndpoint, PostEndpoint):
    """Stop a tensorboard."""

    def post(self, request, *args, **kwargs):
        project = self.project
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
                },
                countdown=conf.get('GLOBAL_COUNTDOWN'))
            auditor.record(event_type=TENSORBOARD_STOPPED_TRIGGERED,
                           instance=tensorboard,
                           target='project',
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
        return Response(status=status.HTTP_200_OK)


class StartNotebookView(ProjectEndpoint, PostEndpoint):
    """Start a notebook."""
    serializer_class = NotebookJobSerializer

    @staticmethod
    def _get_default_notebook_config():
        if not conf.get('NOTEBOOK_DOCKER_IMAGE'):
            raise ValidationError('Please provide a polyaxonfile, or set a default notebook image.')
        specification = NotebookSpecification.create_specification(
            {'image': conf.get('NOTEBOOK_DOCKER_IMAGE')})
        return {'config': specification}

    def _create_notebook(self, project):
        config = self.request.data or self._get_default_notebook_config()
        serializer = self.get_serializer(data=config)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user, project=project)
        auditor.record(event_type=NOTEBOOK_STARTED_TRIGGERED,
                       instance=instance,
                       target='project',
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)

    def post(self, request, *args, **kwargs):
        if self.project.has_notebook:
            return Response(data='Notebook is already running', status=status.HTTP_200_OK)
        self._create_notebook(self.project)
        self.project.clear_cached_properties()
        notebook = self.project.notebook
        if not notebook.is_running:
            celery_app.send_task(
                SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD,
                kwargs={'notebook_job_id': notebook.id},
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_201_CREATED)


class StopNotebookView(ProjectEndpoint, PostEndpoint):
    """Stop a tensorboard."""

    def handle_code(self, request):
        commit = request.data.get('commit')
        commit = to_bool(commit) if commit is not None else True
        if commit and conf.get('MOUNT_CODE_IN_NOTEBOOKS') and self.project.has_repo:
            # Commit changes
            git.commit(self.project.repo.path, request.user.email, request.user.username)
        else:
            # Reset changes
            git.undo(self.project.repo.path)

    def post(self, request, *args, **kwargs):
        if self.project.has_notebook:
            try:
                if conf.get('MOUNT_CODE_IN_NOTEBOOKS') and self.project.has_repo:
                    self.handle_code(request)
            except FileNotFoundError:
                # Git probably was not found
                pass
            celery_app.send_task(
                SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
                kwargs={
                    'project_name': self.project.unique_name,
                    'project_uuid': self.project.uuid.hex,
                    'notebook_job_name': self.project.notebook.unique_name,
                    'notebook_job_uuid': self.project.notebook.uuid.hex,
                    'update_status': True
                },
                countdown=conf.get('GLOBAL_COUNTDOWN'))
            auditor.record(event_type=NOTEBOOK_STOPPED_TRIGGERED,
                           instance=self.project.notebook,
                           target='project',
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           countdown=1)
        elif self.project.notebook and self.project.notebook.is_stoppable:
            self.project.notebook.set_status(status=ExperimentLifeCycle.STOPPED,
                                             message='Notebook was stopped')
        return Response(status=status.HTTP_200_OK)


class PluginJobView(ProjectEndpoint, ProtectedView):
    def get_instance(self):
        return self.project

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

    def get(self, request, *args, **kwargs):
        instance = self.get_instance()
        if not self.has_plugin_job(instance):
            raise Http404
        # self.audit(instance=instance)  TODO add later
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
        if instance.has_notebook:
            backend = instance.notebook.specification.backend or conf.get('NOTEBOOK_BACKEND')
        else:
            backend = conf.get('NOTEBOOK_BACKEND')
        if backend == NotebookBackend.LAB:
            return 'lab'
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
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)


class TensorboardView(PluginJobView):
    def get_instance(self):
        experiment_id = self.kwargs.get('experiment_id')
        group_id = self.kwargs.get('group_id')

        if experiment_id:
            return get_object_or_404(Experiment, project=self.project, id=experiment_id)
        elif group_id:
            return get_object_or_404(ExperimentGroup, project=self.project, id=group_id)

        return self.project

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
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)


class ProjectTensorboardListView(ProjectResourceListEndpoint,
                                 ListEndpoint,
                                 CreateEndpoint):
    """List an tensorboards under a project."""
    queryset = TensorboardJob.objects
    serializer_class = ProjectTensorboardJobSerializer
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'tensorboard'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')

    def filter_queryset(self, queryset):
        auditor.record(event_type=PROJECT_TENSORBOARDS_VIEWED,
                       instance=self.project,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        return super().filter_queryset(queryset=queryset)


class NotebookImpersonateTokenView(ProjectEndpoint, PostEndpoint):
    """Impersonate a user and return user's token."""
    authentication_classes = [InternalAuthentication, ]
    permission_classes = (IsInitializer,)
    throttle_scope = 'impersonate'

    def post(self, request, *args, **kwargs):
        project = self.project

        if not project.has_notebook or not JobLifeCycle.is_stoppable(project.notebook.last_status):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=project.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

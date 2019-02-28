import logging
import os
from typing import Optional

from hestia.bool_utils import to_bool
from polystores.exceptions import PolyaxonStoresException
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

import auditor
import conf
import stores

from api.code_reference.serializers import CodeReferenceSerializer
from api.endpoint.base import (
    CreateEndpoint,
    DestroyEndpoint,
    ListEndpoint,
    PostEndpoint,
    RetrieveEndpoint,
    UpdateEndpoint
)
from api.endpoint.experiment import (
    ExperimentEndpoint,
    ExperimentResourceEndpoint,
    ExperimentResourceListEndpoint
)
from api.endpoint.experiment_job import (
    ExperimentJobEndpoint,
    ExperimentJobResourceEndpoint,
    ExperimentJobResourceListEndpoint
)
from api.endpoint.project import ProjectResourceListEndpoint
from api.experiments import queries
from api.experiments.serializers import (
    BookmarkedExperimentSerializer,
    ExperimentChartViewSerializer,
    ExperimentCreateSerializer,
    ExperimentDeclarationsSerializer,
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentLastMetricSerializer,
    ExperimentMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from api.filters import OrderingFilter, QueryFilter
from api.paginator import LargeLimitOffsetPagination
from api.utils.files import stream_file
from api.utils.gzip import gzip
from api.utils.views.bookmarks_mixin import BookmarkedListMixinView
from api.utils.views.protected import ProtectedView
from constants.experiments import ExperimentLifeCycle
from db.models.experiment_groups import ExperimentGroup
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import (
    Experiment,
    ExperimentChartView,
    ExperimentMetric,
    ExperimentStatus
)
from db.models.tokens import Token
from db.redis.ephemeral_tokens import RedisEphemeralTokens
from db.redis.heartbeat import RedisHeartBeat
from db.redis.tll import RedisTTL
from event_manager.events.chart_view import CHART_VIEW_CREATED, CHART_VIEW_DELETED
from event_manager.events.experiment import (
    EXPERIMENT_ARCHIVED,
    EXPERIMENT_COPIED_TRIGGERED,
    EXPERIMENT_DELETED_TRIGGERED,
    EXPERIMENT_JOBS_VIEWED,
    EXPERIMENT_LOGS_VIEWED,
    EXPERIMENT_METRICS_VIEWED,
    EXPERIMENT_OUTPUTS_DOWNLOADED,
    EXPERIMENT_RESTARTED_TRIGGERED,
    EXPERIMENT_RESTORED,
    EXPERIMENT_RESUMED_TRIGGERED,
    EXPERIMENT_STATUSES_VIEWED,
    EXPERIMENT_STOPPED_TRIGGERED,
    EXPERIMENT_UPDATED,
    EXPERIMENT_VIEWED
)
from event_manager.events.experiment_group import EXPERIMENT_GROUP_EXPERIMENTS_VIEWED
from event_manager.events.experiment_job import (
    EXPERIMENT_JOB_STATUSES_VIEWED,
    EXPERIMENT_JOB_VIEWED
)
from event_manager.events.project import PROJECT_EXPERIMENTS_VIEWED
from libs.archive import archive_logs_file, archive_outputs, archive_outputs_file
from libs.spec_validation import validate_experiment_spec_config
from logs_handlers.log_queries.experiment import process_logs
from logs_handlers.log_queries.experiment_job import process_logs as process_experiment_job_logs
from polyaxon.celery_api import celery_app
from polyaxon.settings import LogsCeleryTasks, SchedulerCeleryTasks
from schemas.tasks import TaskType
from scopes.authentication.ephemeral import EphemeralAuthentication
from scopes.authentication.internal import InternalAuthentication
from scopes.permissions.ephemeral import IsEphemeral
from scopes.permissions.internal import IsAuthenticatedOrInternal, IsInitializer
from scopes.permissions.projects import get_permissible_project
from stores.exceptions import VolumeNotFoundError  # noqa

_logger = logging.getLogger("polyaxon.views.experiments")


class ExperimentListView(ListAPIView):
    """List all experiments for a user."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)


class ProjectExperimentListView(BookmarkedListMixinView,
                                ProjectResourceListEndpoint,
                                ListEndpoint,
                                CreateEndpoint):
    """
    get:
        List experiments under a project.

    post:
        Create an experiment under a project.
    """
    queryset = queries.experiments
    serializer_class = BookmarkedExperimentSerializer
    metrics_serializer_class = ExperimentLastMetricSerializer
    declarations_serializer_class = ExperimentDeclarationsSerializer
    create_serializer_class = ExperimentCreateSerializer
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'experiment'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')
    ordering_proxy_fields = {'metric': 'last_metric'}

    def get_serializer_class(self):
        if self.create_serializer_class and self.request.method.lower() == 'post':
            return self.create_serializer_class

        metrics_only = to_bool(self.request.query_params.get('metrics', None),
                               handle_none=True,
                               exception=ValidationError)
        if metrics_only:
            return self.metrics_serializer_class

        declarations_only = to_bool(self.request.query_params.get('declarations', None),
                                    handle_none=True,
                                    exception=ValidationError)
        if declarations_only:
            return self.declarations_serializer_class

        return self.serializer_class

    @property
    def paginator(self):
        if self.request.query_params.get('all', None):
            self.pagination_class = LargeLimitOffsetPagination
        return super().paginator

    def get_group(self, project, group_id):
        group = get_object_or_404(ExperimentGroup, project=project, id=group_id)
        auditor.record(event_type=EXPERIMENT_GROUP_EXPERIMENTS_VIEWED,
                       instance=group,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)

        return group

    def filter_queryset(self, queryset):
        independent = to_bool(self.request.query_params.get('independent', None),
                              handle_none=True,
                              exception=ValidationError)
        group_id = self.request.query_params.get('group', None)
        if independent and group_id:
            raise ValidationError('You cannot filter for independent experiments and '
                                  'group experiments at the same time.')
        queryset = queryset.filter(project=self.project)
        if independent:
            queryset = queryset.filter(experiment_group__isnull=True)
        if group_id:
            group = self.get_group(project=self.project, group_id=group_id)
            if group.is_study:
                queryset = queryset.filter(experiment_group=group)
            elif group.is_selection:
                queryset = group.selection_experiments.all()
            else:
                raise ValidationError('Invalid group.')
        auditor.record(event_type=PROJECT_EXPERIMENTS_VIEWED,
                       instance=self.project,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        ttl = self.request.data.get(RedisTTL.TTL_KEY)
        if ttl:
            try:
                ttl = RedisTTL.validate_ttl(ttl)
            except ValueError:
                raise ValidationError('ttl must be an integer.')
        group = self.request.data.get('experiment_group')
        if group:
            try:
                group = ExperimentGroup.objects.get(id=group, project=self.project)
            except ExperimentGroup.DoesNotExist:
                raise ValidationError('Received an invalid group.')
            if group.is_selection:
                self.request.data.pop('experiment_group')

        instance = serializer.save(user=self.request.user, project=self.project)
        if group and group.is_selection:  # Add the experiment to the group selection
            group.selection_experiments.add(instance)
        if ttl:
            RedisTTL.set_for_experiment(experiment_id=instance.id, value=ttl)

    @gzip()
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExperimentDetailView(ExperimentEndpoint,
                           RetrieveEndpoint,
                           DestroyEndpoint,
                           UpdateEndpoint):
    """
    get:
        Get an experiment details.
    patch:
        Update an experiment details.
    delete:
        Delete an experiment.
    """
    queryset = queries.experiments_details
    serializer_class = ExperimentDetailSerializer
    AUDITOR_EVENT_TYPES = {
        'GET': EXPERIMENT_VIEWED,
        'UPDATE': EXPERIMENT_UPDATED,
        'DELETE': EXPERIMENT_DELETED_TRIGGERED
    }

    def perform_destroy(self, instance):
        instance.archive()
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_SCHEDULE_DELETION,
            kwargs={'experiment_id': instance.id, 'immediate': True},
            countdown=conf.get('GLOBAL_COUNTDOWN'))


class ExperimentArchiveView(ExperimentEndpoint, CreateEndpoint):
    """Restore an experiment."""
    serializer_class = ExperimentSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_ARCHIVED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_SCHEDULE_DELETION,
            kwargs={'experiment_id': obj.id, 'immediate': False},
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ExperimentRestoreView(ExperimentEndpoint, CreateEndpoint):
    """Restore an experiment."""
    queryset = Experiment.all
    serializer_class = ExperimentSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_RESTORED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        obj.restore()
        return Response(status=status.HTTP_200_OK)


class ExperimentCloneView(ExperimentEndpoint, CreateEndpoint):
    serializer_class = ExperimentSerializer
    event_type = None

    def clone(self, obj, config, declarations, update_code_reference, description):
        pass

    def post(self, request, *args, **kwargs):
        ttl = self.request.data.get(RedisTTL.TTL_KEY)
        if ttl:
            try:
                ttl = RedisTTL.validate_ttl(ttl)
            except ValueError:
                raise ValidationError('ttl must be an integer.')

        obj = self.get_object()
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)

        description = None
        config = None
        declarations = None
        update_code_reference = False
        if 'config' in request.data:
            spec = validate_experiment_spec_config(
                [obj.specification.parsed_data, request.data['config']], raise_for_rest=True)
            config = spec.parsed_data
            declarations = spec.declarations
        if 'update_code' in request.data:
            update_code_reference = to_bool(request.data['update_code'],
                                            handle_none=True,
                                            exception=ValidationError)
        if 'description' in request.data:
            description = request.data['description']
        new_obj = self.clone(obj=obj,
                             config=config,
                             declarations=declarations,
                             update_code_reference=update_code_reference,
                             description=description)
        if ttl:
            RedisTTL.set_for_experiment(experiment_id=new_obj.id, value=ttl)
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class ExperimentRestartView(ExperimentCloneView):
    """Restart an experiment."""
    serializer_class = ExperimentSerializer
    event_type = EXPERIMENT_RESTARTED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.restart(user=self.request.user,
                           config=config,
                           declarations=declarations,
                           update_code_reference=update_code_reference,
                           description=description)


class ExperimentResumeView(ExperimentCloneView):
    """Resume an experiment."""
    serializer_class = ExperimentSerializer
    event_type = EXPERIMENT_RESUMED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.resume(user=self.request.user,
                          config=config,
                          declarations=declarations,
                          update_code_reference=update_code_reference,
                          description=description)


class ExperimentCopyView(ExperimentCloneView):
    """Copy an experiment."""
    serializer_class = ExperimentSerializer
    event_type = EXPERIMENT_COPIED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.copy(user=self.request.user,
                        config=config,
                        declarations=declarations,
                        update_code_reference=update_code_reference,
                        description=description)


class ExperimentCodeReferenceView(ExperimentEndpoint, CreateEndpoint, RetrieveEndpoint):
    """
    post:
        Create an experiment metric.
    """
    serializer_class = CodeReferenceSerializer

    def perform_create(self, serializer):
        experiment = self.get_object()
        instance = serializer.save()
        experiment.code_reference = instance
        experiment.save(update_fields=['code_reference'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance.code_reference)
        return Response(serializer.data)


class ExperimentViewMixin(object):
    """A mixin to filter by experiment."""
    project = None
    experiment = None

    def get_experiment(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        experiment_id = self.kwargs['experiment_id']
        self.experiment = get_object_or_404(queries.experiments_auditing,
                                            project=self.project,
                                            id=experiment_id)
        return self.experiment

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentOutputsTreeView(ExperimentEndpoint, RetrieveEndpoint):
    """
    get:
        Returns a the outputs directory tree.
    """
    def get(self, request, *args, **kwargs):
        try:
            store_manager = stores.get_outputs_store(
                persistence_outputs=self.experiment.persistence_outputs)
        except (PolyaxonStoresException, VolumeNotFoundError) as e:
            raise ValidationError(e)
        experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name,
            original_name=self.experiment.original_unique_name,
            cloning_strategy=self.experiment.cloning_strategy)
        if request.query_params.get('path'):
            experiment_outputs_path = os.path.join(experiment_outputs_path,
                                                   request.query_params.get('path'))
        try:
            data = store_manager.ls(experiment_outputs_path)
        except VolumeNotFoundError:
            raise ValidationError('Store manager could not load the volume requested,'
                                  ' to get the outputs data.')
        except Exception:
            raise ValidationError('Experiment outputs path does not exists or bad configuration.')
        return Response(data=data, status=200)


class ExperimentOutputsFilesView(ExperimentEndpoint, RetrieveEndpoint):
    """
    get:
        Returns a the outputs files content.
    """

    def get(self, request, *args, **kwargs):
        filepath = request.query_params.get('path')
        if not filepath:
            raise ValidationError('Files view expect a path to the file.')

        experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name,
            original_name=self.experiment.original_unique_name,
            cloning_strategy=self.experiment.cloning_strategy)

        download_filepath = archive_outputs_file(
            persistence_outputs=self.experiment.persistence_outputs,
            outputs_path=experiment_outputs_path,
            namepath=self.experiment.unique_name,
            filepath=filepath)

        if not download_filepath:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Outputs file not found: log_path={}'.format(download_filepath))

        return stream_file(file_path=download_filepath, logger=_logger)


class ExperimentStatusListView(ExperimentResourceListEndpoint,
                               ListEndpoint,
                               CreateEndpoint):
    """
    get:
        List all statuses of an experiment.
    post:
        Create an experiment status.
    """
    queryset = ExperimentStatus.objects.order_by('created_at')
    serializer_class = ExperimentStatusSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(experiment=self.experiment)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_STATUSES_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentMetricListView(ExperimentResourceEndpoint,
                               ListEndpoint,
                               CreateEndpoint):
    """
    get:
        List all metrics of an experiment.
    post:
        Create an experiment metric.
    """
    queryset = ExperimentMetric.objects
    serializer_class = ExperimentMetricSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]
    pagination_class = LargeLimitOffsetPagination
    throttle_scope = 'high'

    def perform_create(self, serializer):
        serializer.save(experiment=self.experiment)

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_SET_METRICS,
                kwargs={
                    'experiment_id': self.experiment.id,
                    'data': request.data
                },
                countdown=conf.get('GLOBAL_COUNTDOWN'))
            return Response(status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @gzip()
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_METRICS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentStatusDetailView(ExperimentResourceEndpoint, RetrieveEndpoint):
    """Get experiment status details."""
    queryset = ExperimentStatus.objects
    serializer_class = ExperimentStatusSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'


class ExperimentJobListView(ExperimentResourceListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List all jobs of an experiment.
    post:
        Create an experiment job.
    """
    queryset = ExperimentJob.objects.order_by('-updated_at')
    serializer_class = ExperimentJobSerializer
    create_serializer_class = ExperimentJobDetailSerializer

    def perform_create(self, serializer):
        serializer.save(experiment=self.experiment)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOBS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentJobDetailView(ExperimentJobEndpoint,
                              RetrieveEndpoint,
                              UpdateEndpoint,
                              DestroyEndpoint):
    """
    get:
        Get experiment job details.
    patch:
        Update an experiment job details.
    delete:
        Delete an experiment job.
    """
    serializer_class = ExperimentJobDetailSerializer
    lookup_field = 'id'
    AUDITOR_EVENT_TYPES = {'GET': EXPERIMENT_JOB_VIEWED}


def get_experiment_logs_path(experiment: Experiment) -> Optional[str]:
    experiment_name = experiment.unique_name
    if experiment.is_done:
        log_path = stores.get_experiment_logs_path(experiment_name=experiment_name, temp=False)
        logs_path = archive_logs_file(
            log_path=log_path,
            namepath=experiment_name)
    elif experiment.in_cluster:
        process_logs(experiment=experiment, temp=True)
        logs_path = stores.get_experiment_logs_path(experiment_name=experiment_name, temp=True)
    else:
        return None

    return logs_path


def get_experiment_job_logs_path(experiment: Experiment, job: ExperimentJob) -> Optional[str]:
    if not job:
        return None
    job_name = job.unique_name
    if experiment.is_done:
        log_path = stores.get_experiment_job_logs_path(experiment_job_name=job_name, temp=False)
        logs_path = archive_logs_file(
            log_path=log_path,
            namepath=job_name)
    elif experiment.in_cluster:
        process_experiment_job_logs(experiment_job=job, temp=True)
        logs_path = stores.get_experiment_job_logs_path(experiment_job_name=job_name, temp=True)
    else:
        logs_path = None

    return logs_path


class ExperimentLogsView(ExperimentEndpoint, RetrieveEndpoint, PostEndpoint):
    """
    get:
        Get experiment logs.
    post:
        Post experiment logs.
    """

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=EXPERIMENT_LOGS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        if self.experiment.is_distributed:
            job = self.experiment.jobs.filter(role=TaskType.MASTER).first()
            logs_path = get_experiment_job_logs_path(experiment=self.experiment, job=job)
        else:
            logs_path = get_experiment_logs_path(experiment=self.experiment)
        if not logs_path:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Experiment has no logs.')

        return stream_file(file_path=logs_path, logger=_logger)

    def post(self, request, *args, **kwargs):
        log_lines = request.data
        if not log_lines or not isinstance(log_lines, (str, list)):
            raise ValidationError('Logs handler expects `data` to be a string or list of strings.')
        if isinstance(log_lines, list):
            log_lines = '\n'.join(log_lines)
        celery_app.send_task(
            LogsCeleryTasks.LOGS_HANDLE_EXPERIMENT_JOB,
            kwargs={
                'experiment_name': self.experiment.unique_name,
                'experiment_uuid': self.experiment.uuid.hex,
                'log_lines': log_lines,
                'temp': True
            })
        return Response(status=status.HTTP_200_OK)


class ExperimentHeartBeatView(ExperimentEndpoint, PostEndpoint):
    """
    post:
        Post a heart beat ping.
    """
    permission_classes = ExperimentEndpoint.permission_classes + (IsAuthenticatedOrInternal,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]

    def post(self, request, *args, **kwargs):
        RedisHeartBeat.experiment_ping(experiment_id=self.experiment.id)
        return Response(status=status.HTTP_200_OK)


class ExperimentJobViewMixin(object):
    """A mixin to filter by experiment job."""
    project = None
    experiment = None
    job = None

    def get_experiment(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        experiment_id = self.kwargs['experiment_id']
        self.experiment = get_object_or_404(Experiment, project=self.project, id=experiment_id)
        return self.experiment

    def get_job(self):
        job_id = self.kwargs['id']
        self.job = get_object_or_404(ExperimentJob,
                                     id=job_id,
                                     experiment=self.get_experiment())
        return self.job

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class ExperimentJobStatusListView(ExperimentJobResourceListEndpoint, ListEndpoint, CreateEndpoint):
    """
    get:
        List all statuses of experiment job.
    post:
        Create an experiment job status.
    """
    queryset = ExperimentJobStatus.objects.order_by('created_at')
    serializer_class = ExperimentJobStatusSerializer

    def perform_create(self, serializer):
        serializer.save(job=self.job)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        return response


class ExperimentJobStatusDetailView(ExperimentJobResourceEndpoint,
                                    RetrieveEndpoint,
                                    UpdateEndpoint):
    """
    get:
        Get experiment job status details.
    patch:
        Update an experiment job status details.
    """
    queryset = ExperimentJobStatus.objects
    serializer_class = ExperimentJobStatusSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'


class ExperimentJobLogsView(ExperimentJobResourceEndpoint,
                            RetrieveEndpoint,
                            UpdateEndpoint):
    """
    get:
        Get experiment job status details.
    patch:
        Update an experiment job status details.
    """
    queryset = ExperimentJobStatus.objects
    serializer_class = ExperimentJobStatusSerializer
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=EXPERIMENT_LOGS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        if self.experiment.is_distributed:
            logs_path = get_experiment_job_logs_path(experiment=self.experiment, job=self.job)
        else:
            logs_path = get_experiment_logs_path(experiment=self.experiment)
        if not logs_path:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Experiment has no logs.')

        return stream_file(file_path=logs_path, logger=_logger)


class ExperimentStopView(ExperimentEndpoint, CreateEndpoint):
    """Stop an experiment."""
    serializer_class = ExperimentSerializer

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id,
                       actor_name=request.user.username)
        group = obj.experiment_group
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={
                'project_name': self.project.unique_name,
                'project_uuid': self.project.uuid.hex,
                'experiment_name': obj.unique_name,
                'experiment_uuid': obj.uuid.hex,
                'experiment_group_name': group.unique_name if group else None,
                'experiment_group_uuid': group.uuid.hex if group else None,
                'specification': obj.config,
                'update_status': True,
                'collect_logs': True,
            },
            countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ExperimentStopManyView(ProjectResourceListEndpoint, PostEndpoint):
    """Stop a group of experiments."""
    queryset = queries.experiments_auditing

    def post(self, request, *args, **kwargs):
        experiments = self.queryset.filter(project=self.project,
                                           id__in=request.data.get('ids', []))
        for experiment in experiments:
            auditor.record(event_type=EXPERIMENT_STOPPED_TRIGGERED,
                           instance=experiment,
                           actor_id=request.user.id,
                           actor_name=request.user.username)
            group = experiment.experiment_group
            celery_app.send_task(
                SchedulerCeleryTasks.EXPERIMENTS_STOP,
                kwargs={
                    'project_name': self.project.unique_name,
                    'project_uuid': self.project.uuid.hex,
                    'experiment_name': experiment.unique_name,
                    'experiment_uuid': experiment.uuid.hex,
                    'experiment_group_name': group.unique_name if group else None,
                    'experiment_group_uuid': group.uuid.hex if group else None,
                    'specification': experiment.config,
                    'update_status': True,
                    'collect_logs': True,
                },
                countdown=conf.get('GLOBAL_COUNTDOWN'))
        return Response(status=status.HTTP_200_OK)


class ExperimentDeleteManyView(ProjectResourceListEndpoint, PostEndpoint):
    """Delete a group of experiments."""
    queryset = queries.experiments_auditing

    def delete(self, request, *args, **kwargs):
        experiments = queries.experiments_auditing.filter(project=self.project,
                                                          id__in=request.data.get('ids', []))
        for experiment in experiments:
            auditor.record(event_type=EXPERIMENT_DELETED_TRIGGERED,
                           instance=experiment,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username)
            experiment.delete()
        return Response(status=status.HTTP_200_OK)


class ExperimentDownloadOutputsView(ExperimentEndpoint, ProtectedView):
    """Download outputs of an experiment."""
    HANDLE_UNAUTHENTICATED = False

    def get(self, request, *args, **kwargs):
        auditor.record(event_type=EXPERIMENT_OUTPUTS_DOWNLOADED,
                       instance=self.experiment,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username)
        experiment_outputs_path = stores.get_experiment_outputs_path(
            persistence=self.experiment.persistence_outputs,
            experiment_name=self.experiment.unique_name,
            original_name=self.experiment.original_unique_name,
            cloning_strategy=self.experiment.cloning_strategy)
        archived_path, archive_name = archive_outputs(
            outputs_path=experiment_outputs_path,
            name=self.experiment.unique_name)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))


class ExperimentEphemeralTokenView(ExperimentEndpoint, PostEndpoint):
    """Validate scope token and return user's token."""
    authentication_classes = [EphemeralAuthentication, ]
    permission_classes = (IsEphemeral,)
    throttle_scope = 'ephemeral'
    lookup_url_kwarg = 'experiment_id'

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.scope is None:
            return Response(status=status.HTTP_403_FORBIDDEN)

        experiment = self.get_object()

        if experiment.last_status not in [ExperimentLifeCycle.SCHEDULED,
                                          ExperimentLifeCycle.STARTING,
                                          ExperimentLifeCycle.RUNNING]:
            return Response(status=status.HTTP_403_FORBIDDEN)

        scope = RedisEphemeralTokens.get_scope(user=experiment.user.id,
                                               model='experiment',
                                               object_id=experiment.id)
        if sorted(user.scope) != sorted(scope):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=experiment.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ExperimentImpersonateTokenView(ExperimentEndpoint, PostEndpoint):
    """Impersonate a user and return user's token."""
    authentication_classes = [InternalAuthentication, ]
    permission_classes = (IsInitializer,)
    throttle_scope = 'impersonate'
    lookup_url_kwarg = 'experiment_id'

    def post(self, request, *args, **kwargs):
        experiment = self.get_object()

        if not ExperimentLifeCycle.is_stoppable(experiment.last_status):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=experiment.user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ExperimentChartViewListView(ExperimentResourceListEndpoint,
                                  ListEndpoint,
                                  CreateEndpoint):
    """
    get:
        List all chart views of an experiment.
    post:
        Create an experiment chart view.
    """
    queryset = ExperimentChartView.objects
    serializer_class = ExperimentChartViewSerializer
    pagination_class = LargeLimitOffsetPagination

    def perform_create(self, serializer):
        instance = serializer.save(experiment=self.experiment)
        auditor.record(event_type=CHART_VIEW_CREATED,
                       instance=instance,
                       actor_id=self.request.user.id,
                       actor_name=self.request.user.username,
                       experiment=self.experiment)


class ExperimentChartViewDetailView(ExperimentResourceEndpoint,
                                    RetrieveEndpoint,
                                    UpdateEndpoint,
                                    DestroyEndpoint):
    """
    get:
        Get experiment chart view details.
    patch:
        Update an experiment chart view details.
    delete:
        Delete an experiment chart view.
    """
    queryset = ExperimentChartView.objects
    serializer_class = ExperimentChartViewSerializer
    lookup_field = 'id'

    def get_object(self):
        if self._object:
            return self._object
        self._object = super().get_object()
        if self.request.method == 'DELETE':
            auditor.record(event_type=CHART_VIEW_DELETED,
                           instance=self._object,
                           actor_id=self.request.user.id,
                           actor_name=self.request.user.username,
                           group=self._object)
        return self._object

import logging
import mimetypes
import os

from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from django.http import StreamingHttpResponse

import auditor

from api.experiments.serializers import (
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
from api.utils.views import AuditorMixinView, ListCreateAPIView, ProtectedView
from db.models.experiment_groups import ExperimentGroup
from db.models.experiment_jobs import ExperimentJob, ExperimentJobStatus
from db.models.experiments import Experiment, ExperimentMetric, ExperimentStatus
from event_manager.events.experiment import (
    EXPERIMENT_COPIED_TRIGGERED,
    EXPERIMENT_CREATED,
    EXPERIMENT_DELETED_TRIGGERED,
    EXPERIMENT_JOBS_VIEWED,
    EXPERIMENT_LOGS_VIEWED,
    EXPERIMENT_OUTPUTS_DOWNLOADED,
    EXPERIMENT_RESTARTED_TRIGGERED,
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
from libs.archive import archive_experiment_outputs
from libs.paths.experiments import get_experiment_logs_path
from libs.permissions.authentication import InternalAuthentication
from libs.permissions.internal import IsAuthenticatedOrInternal
from libs.permissions.projects import get_permissible_project
from libs.spec_validation import validate_experiment_spec_config
from libs.utils import to_bool
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

_logger = logging.getLogger("polyaxon.views.experiments")


class ExperimentListView(ListAPIView):
    """List all experiments for a user."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)


class ProjectExperimentListView(ListCreateAPIView):
    """
    get:
        List experiments under a project.

    post:
        Create an experiment under a project.
    """
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    metrics_serializer_class = ExperimentLastMetricSerializer
    declarations_serializer_class = ExperimentDeclarationsSerializer
    create_serializer_class = ExperimentCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (QueryFilter, OrderingFilter,)
    query_manager = 'experiment'
    ordering = ('-updated_at',)
    ordering_fields = ('created_at', 'updated_at', 'started_at', 'finished_at')
    ordering_proxy_fields = {'metric': 'metric__values'}

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

    def get_group(self, project, group_id):
        group = get_object_or_404(ExperimentGroup, project=project, id=group_id)
        auditor.record(event_type=EXPERIMENT_GROUP_EXPERIMENTS_VIEWED,
                       instance=group,
                       actor_id=self.request.user.id)

        return group

    def filter_queryset(self, queryset):
        independent = to_bool(self.request.query_params.get('independent', None),
                              handle_none=True,
                              exception=ValidationError)
        group_id = self.request.query_params.get('group', None)
        if independent and group_id:
            raise ValidationError('You cannot filter for independent experiments and '
                                  'group experiments at the same time.')
        project = get_permissible_project(view=self)
        queryset = queryset.filter(project=project)
        if independent:
            queryset = queryset.filter(experiment_group__isnull=True)
        if group_id:
            group = self.get_group(project=project, group_id=group_id)
            queryset = queryset.filter(experiment_group=group)
        auditor.record(event_type=PROJECT_EXPERIMENTS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id)
        return super().filter_queryset(queryset=queryset)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user,
                                   project=get_permissible_project(view=self))
        auditor.record(event_type=EXPERIMENT_CREATED, instance=instance)


class ExperimentDetailView(AuditorMixinView, RetrieveUpdateDestroyAPIView):
    """
    get:
        Get an experiment details.
    patch:
        Update an experiment details.
    delete:
        Delete an experiment.
    """
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    instance = None
    get_event = EXPERIMENT_VIEWED
    update_event = EXPERIMENT_UPDATED
    delete_event = EXPERIMENT_DELETED_TRIGGERED

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))


class ExperimentCloneView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    event_type = None

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def clone(self, obj, config, declarations, update_code_reference, description):
        pass

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=self.event_type,
                       instance=obj,
                       actor_id=self.request.user.id)

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
        serializer = self.get_serializer(new_obj)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)


class ExperimentRestartView(ExperimentCloneView):
    """Restart an experiment."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    event_type = EXPERIMENT_RESTARTED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.restart(user=self.request.user,
                           config=config,
                           declarations=declarations,
                           update_code_reference=update_code_reference,
                           description=description)


class ExperimentResumeView(ExperimentCloneView):
    """Resume an experiment."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    event_type = EXPERIMENT_RESUMED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.resume(user=self.request.user,
                          config=config,
                          declarations=declarations,
                          update_code_reference=update_code_reference,
                          description=description)


class ExperimentCopyView(ExperimentCloneView):
    """Copy an experiment."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    event_type = EXPERIMENT_COPIED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.copy(user=self.request.user,
                        config=config,
                        declarations=declarations,
                        update_code_reference=update_code_reference,
                        description=description)


class ExperimentViewMixin(object):
    """A mixin to filter by experiment."""
    project = None
    experiment = None

    def get_experiment(self):
        # Get project and check access
        self.project = get_permissible_project(view=self)
        experiment_id = self.kwargs['experiment_id']
        self.experiment = get_object_or_404(Experiment, project=self.project, id=experiment_id)
        return self.experiment

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ExperimentViewMixin, ListCreateAPIView):
    """
    get:
        List all statuses of an experiment.
    post:
        Create an experiment status.
    """
    queryset = ExperimentStatus.objects.order_by('created_at').all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_STATUSES_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id)
        return response


class ExperimentMetricListView(ExperimentViewMixin, ListCreateAPIView):
    """
    get:
        List all metrics of an experiment.
    post:
        Create an experiment metric.
    """
    queryset = ExperimentMetric.objects.all()
    serializer_class = ExperimentMetricSerializer
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        InternalAuthentication,
    ]
    permission_classes = (IsAuthenticatedOrInternal,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(ExperimentViewMixin, RetrieveAPIView):
    """Get experiment status details."""
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentJobListView(ExperimentViewMixin, ListCreateAPIView):
    """
    get:
        List all jobs of an experiment.
    post:
        Create an experiment job.
    """
    queryset = ExperimentJob.objects.order_by('-updated_at').all()
    serializer_class = ExperimentJobSerializer
    create_serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOBS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id)
        return response


class ExperimentJobDetailView(AuditorMixinView, ExperimentViewMixin, RetrieveUpdateDestroyAPIView):
    """
    get:
        Get experiment job details.
    patch:
        Update an experiment job details.
    delete:
        Delete an experiment job.
    """
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'
    get_event = EXPERIMENT_JOB_VIEWED


class ExperimentLogsView(ExperimentViewMixin, RetrieveAPIView):
    """Get experiment logs."""
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        experiment = self.get_experiment()
        auditor.record(event_type=EXPERIMENT_LOGS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id)
        log_path = get_experiment_logs_path(experiment.unique_name)

        filename = os.path.basename(log_path)
        chunk_size = 8192
        try:
            wrapped_file = FileWrapper(open(log_path, 'rb'), chunk_size)
            response = StreamingHttpResponse(wrapped_file,
                                             content_type=mimetypes.guess_type(log_path)[0])
            response['Content-Length'] = os.path.getsize(log_path)
            response['Content-Disposition'] = "attachment; filename={}".format(filename)
            return response
        except FileNotFoundError:
            _logger.warning('Log file not found: log_path=%s', log_path)
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='Log file not found: log_path={}'.format(log_path))


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


class ExperimentJobStatusListView(ExperimentJobViewMixin, ListCreateAPIView):
    """
    get:
        List all statuses of experiment job.
    post:
        Create an experiment job status.
    """
    queryset = ExperimentJobStatus.objects.order_by('created_at').all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(job=self.get_job())

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id)
        return response


class ExperimentJobStatusDetailView(ExperimentJobViewMixin, RetrieveUpdateAPIView):
    """
    get:
        Get experiment job status details.
    patch:
        Update an experiment job status details.
    """
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentStopView(CreateAPIView):
    """Stop an experiment."""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id)
        group = obj.experiment_group
        celery_app.send_task(
            SchedulerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={
                'project_name': obj.project.unique_name,
                'project_uuid': obj.project.uuid.hex,
                'experiment_name': obj.unique_name,
                'experiment_uuid': obj.uuid.hex,
                'experiment_group_name': group.unique_name if group else None,
                'experiment_group_uuid': group.uuid.hex if group else None,
                'specification': obj.config,
                'update_status': True
            })
        return Response(status=status.HTTP_200_OK)


class DownloadOutputsView(ProtectedView):
    """Download outputs of an experiment."""
    permission_classes = (IsAuthenticated,)
    HANDLE_UNAUTHENTICATED = False

    def get_object(self):
        project = get_permissible_project(view=self)
        experiment = get_object_or_404(Experiment, project=project, id=self.kwargs['id'])
        auditor.record(event_type=EXPERIMENT_OUTPUTS_DOWNLOADED,
                       instance=experiment,
                       actor_id=self.request.user.id)
        return experiment

    def get(self, request, *args, **kwargs):
        experiment = self.get_object()
        archived_path, archive_name = archive_experiment_outputs(
            persistence_outputs=experiment.persistence_outputs,
            experiment_name=experiment.unique_name)
        return self.redirect(path='{}/{}'.format(archived_path, archive_name))

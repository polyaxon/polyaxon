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

from django.http import StreamingHttpResponse

import auditor

from event_manager.events.experiment import (
    EXPERIMENT_COPIED_TRIGGERED,
    EXPERIMENT_CREATED,
    EXPERIMENT_DELETED_TRIGGERED,
    EXPERIMENT_JOBS_VIEWED,
    EXPERIMENT_LOGS_VIEWED,
    EXPERIMENT_RESTARTED_TRIGGERED,
    EXPERIMENT_RESUMED_TRIGGERED,
    EXPERIMENT_STATUSES_VIEWED,
    EXPERIMENT_UPDATED,
    EXPERIMENT_VIEWED,
    EXPERIMENT_STOPPED_TRIGGERED
)
from event_manager.events.experiment_group import EXPERIMENT_GROUP_EXPERIMENTS_VIEWED
from event_manager.events.experiment_job import (
    EXPERIMENT_JOB_STATUSES_VIEWED,
    EXPERIMENT_JOB_VIEWED
)
from event_manager.events.project import PROJECT_EXPERIMENTS_VIEWED
from db.models.experiment_groups import ExperimentGroup
from db.models.experiments import (
    Experiment,
    ExperimentJob,
    ExperimentJobStatus,
    ExperimentMetric,
    ExperimentStatus
)
from experiments.paths import get_experiment_logs_path
from apis.experiments.serializers import (
    ExperimentCreateSerializer,
    ExperimentDetailSerializer,
    ExperimentJobDetailSerializer,
    ExperimentJobSerializer,
    ExperimentJobStatusSerializer,
    ExperimentMetricSerializer,
    ExperimentSerializer,
    ExperimentStatusSerializer
)
from libs.spec_validation import validate_experiment_spec_config
from libs.utils import to_bool
from libs.views import AuditorMixinView, ListCreateAPIView
from permissions.projects import get_permissible_project
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import RunnerCeleryTasks

logger = logging.getLogger("polyaxon.experiments.views")


class ExperimentListView(ListAPIView):
    """List all experiments"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)


class ProjectExperimentListView(ListCreateAPIView):
    """List/Create an experiment under a project"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    create_serializer_class = ExperimentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, queryset):
        independent = self.request.query_params.get('independent', None)
        filters = {}
        if independent is not None and to_bool(independent):
            filters['experiment_group__isnull'] = True
        project = get_permissible_project(view=self)
        auditor.record(event_type=PROJECT_EXPERIMENTS_VIEWED,
                       instance=project,
                       actor_id=self.request.user.id)
        return queryset.filter(project=project, **filters)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user, project=get_permissible_project(view=self))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        auditor.record(event_type=EXPERIMENT_CREATED, instance=instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupExperimentListView(ListAPIView):
    """List all experiments under a group"""
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)

    def get_group(self):
        sequence = self.kwargs['sequence']
        # Get project and check permissions
        project = get_permissible_project(view=self)
        group = get_object_or_404(ExperimentGroup, project=project, sequence=sequence)
        auditor.record(event_type=EXPERIMENT_GROUP_EXPERIMENTS_VIEWED,
                       instance=group,
                       actor_id=self.request.user.id)

        return group

    def filter_queryset(self, queryset):
        return queryset.filter(experiment_group=self.get_group())


class ExperimentDetailView(AuditorMixinView, RetrieveUpdateDestroyAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
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
    lookup_field = 'sequence'
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
            try:
                update_code_reference = to_bool(request.data['update_code'])
            except TypeError:
                raise ValidationError('update_code should be a boolean')
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
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
    event_type = EXPERIMENT_RESTARTED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.restart(user=self.request.user,
                           config=config,
                           declarations=declarations,
                           update_code_reference=update_code_reference,
                           description=description)


class ExperimentResumeView(ExperimentCloneView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
    event_type = EXPERIMENT_RESUMED_TRIGGERED

    def clone(self, obj, config, declarations, update_code_reference, description):
        return obj.resume(user=self.request.user,
                          config=config,
                          declarations=declarations,
                          update_code_reference=update_code_reference,
                          description=description)


class ExperimentCopyView(ExperimentCloneView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
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
        sequence = self.kwargs['experiment_sequence']
        self.experiment = get_object_or_404(Experiment, project=self.project, sequence=sequence)
        return self.experiment

    def filter_queryset(self, queryset):
        queryset = super(ExperimentViewMixin, self).filter_queryset(queryset)
        return queryset.filter(experiment=self.get_experiment())


class ExperimentStatusListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())

    def get(self, request, *args, **kwargs):
        response = super(ExperimentStatusListView, self).get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_STATUSES_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id)
        return response


class ExperimentMetricListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentMetric.objects.all()
    serializer_class = ExperimentMetricSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())


class ExperimentStatusDetailView(ExperimentViewMixin, RetrieveAPIView):
    queryset = ExperimentStatus.objects.all()
    serializer_class = ExperimentStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentJobListView(ExperimentViewMixin, ListCreateAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobSerializer
    create_serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(experiment=self.get_experiment())

    def get(self, request, *args, **kwargs):
        response = super(ExperimentJobListView, self).get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOBS_VIEWED,
                       instance=self.experiment,
                       actor_id=request.user.id)
        return response


class ExperimentJobDetailView(AuditorMixinView, ExperimentViewMixin, RetrieveUpdateDestroyAPIView):
    queryset = ExperimentJob.objects.all()
    serializer_class = ExperimentJobDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'
    get_event = EXPERIMENT_JOB_VIEWED


class ExperimentLogsView(ExperimentViewMixin, RetrieveAPIView):
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
            logger.warning('Log file not found: log_path=%s', log_path)
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
        sequence = self.kwargs['experiment_sequence']
        self.experiment = get_object_or_404(Experiment, project=self.project, sequence=sequence)
        return self.experiment

    def get_job(self):
        job_sequence = self.kwargs['sequence']
        self.job = get_object_or_404(ExperimentJob,
                                     sequence=job_sequence,
                                     experiment=self.get_experiment())
        return self.job

    def filter_queryset(self, queryset):
        queryset = super(ExperimentJobViewMixin, self).filter_queryset(queryset)
        return queryset.filter(job=self.get_job())


class ExperimentJobStatusListView(ExperimentJobViewMixin, ListCreateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(job=self.get_job())

    def get(self, request, *args, **kwargs):
        response = super(ExperimentJobStatusListView, self).get(request, *args, **kwargs)
        auditor.record(event_type=EXPERIMENT_JOB_STATUSES_VIEWED,
                       instance=self.job,
                       actor_id=request.user.id)
        return response


class ExperimentJobStatusDetailView(ExperimentJobViewMixin, RetrieveUpdateAPIView):
    queryset = ExperimentJobStatus.objects.all()
    serializer_class = ExperimentJobStatusSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'


class ExperimentStopView(CreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'sequence'

    def filter_queryset(self, queryset):
        return queryset.filter(project=get_permissible_project(view=self))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        auditor.record(event_type=EXPERIMENT_STOPPED_TRIGGERED,
                       instance=obj,
                       actor_id=request.user.id)
        celery_app.send_task(
            RunnerCeleryTasks.EXPERIMENTS_STOP,
            kwargs={'experiment_id': obj.id})
        return Response(status=status.HTTP_200_OK)

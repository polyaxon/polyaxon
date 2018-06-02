{{/*
Celery config
*/}}
{{- define "config.celery" }}
- name: POLYAXON_ROUTING_KEYS_EVENTS_NAMESPACE
  value: "events.namespace"
- name: POLYAXON_ROUTING_KEYS_EVENTS_RESOURCES
  value: "events.resources"
- name: POLYAXON_ROUTING_KEYS_EVENTS_JOB_STATUSES
  value: "events.statuses"
- name: POLYAXON_ROUTING_KEYS_LOGS_SIDECARS
  value: "logs.sidecars"
- name: POLYAXON_QUEUES_REPOS
  value: {{ .Values.queues.repos | quote }}
- name: POLYAXON_QUEUES_SCHEDULER_EXPERIMENTS
  value: {{ .Values.queues.schedulerExperiments | quote }}
- name: POLYAXON_QUEUES_SCHEDULER_EXPERIMENT_GROUPS
  value: {{ .Values.queues.schedulerExperimentGroups | quote }}
- name: POLYAXON_QUEUES_SCHEDULER_PROJECTS
  value: {{ .Values.queues.schedulerProjects | quote }}
- name: POLYAXON_QUEUES_PIPELINES
  value: {{ .Values.queues.pipelines | quote }}
- name: POLYAXON_QUEUES_CRONS_EXPERIMENTS
  value: {{ .Values.queues.cronsExperiments | quote }}
- name: POLYAXON_QUEUES_CRONS_PIPELINES
  value: {{ .Values.queues.cronsPipelines | quote }}
- name: POLYAXON_QUEUES_CRONS_CLUSTERS
  value: {{ .Values.queues.cronsClusters | quote }}
- name: POLYAXON_QUEUES_HP
  value: {{ .Values.queues.hp | quote }}
- name: POLYAXON_QUEUES_EVENTS_NAMESPACE
  value: {{ .Values.queues.eventsNamespace | quote }}
- name: POLYAXON_QUEUES_EVENTS_RESOURCES
  value: {{ .Values.queues.eventsResources | quote }}
- name: POLYAXON_QUEUES_EVENTS_JOB_STATUSES
  value: {{ .Values.queues.eventsJobStatuses | quote }}
- name: POLYAXON_QUEUES_LOGS_SIDECARS
  value: {{ .Values.queues.logsSidecars | quote }}
- name: POLYAXON_QUEUES_STREAM_LOGS_SIDECARS
  value: {{ .Values.queues.streamLogsSidecars | quote }}
- name: POLYAXON_INTERVALS_EXPERIMENTS_SCHEDULER
  value: {{ .Values.intervals.experiments_scheduler | quote }}
- name: POLYAXON_INTERVALS_EXPERIMENTS_SYNC
  value: {{ .Values.intervals.experiments_sync | quote }}
- name: POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_INFO
  value: {{ .Values.intervals.clusters_update_system_info | quote }}
- name: POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_NODES
  value: {{ .Values.intervals.clusters_update_system_nodes | quote }}
- name: POLYAXON_INTERVALS_PIPELINES_SCHEDULER
  value: {{ .Values.intervals.pipelines_scheduler | quote }}
- name: POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY
  value: {{ .Values.intervals.operations_default_retry_delay | quote }}
- name: POLYAXON_INTERVALS_OPERATIONS_MAX_RETRY_DELAY
  value: {{ .Values.intervals.operations_max_retry_delay | quote }}
- name: POLYAXON_CELERY_ALWAYS_EAGER
  value: "false"
- name: POLYAXON_CELERYD_PREFETCH_MULTIPLIER
  value: "4"
{{- end -}}

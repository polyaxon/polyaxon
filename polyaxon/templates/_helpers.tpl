{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "polyaxon.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "polyaxon.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
Return the appropriate apiVersion for networkpolicy.
*/}}
{{- define "networkPolicy.apiVersion" -}}
{{- if and (ge .Capabilities.KubeVersion.Minor "4") (le .Capabilities.KubeVersion.Minor "6") -}}
"extensions/v1beta1"
{{- else if ge .Capabilities.KubeVersion.Minor "7" -}}
"networking.k8s.io/v1"
{{- end -}}
{{- end -}}


{{/*
Postgres
Expand the name of the chart.
*/}}
{{- define "postgresql.name" -}}
{{- "postgresql" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "postgresql.fullname" -}}
{{- $name := "postgresql" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{/*
Redis
Expand the name of the chart.
*/}}
{{- define "redis.name" -}}
{{- "redis" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "redis.fullname" -}}
{{- $name := default "redis" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}



{{/*
registry
Expand the name of the chart.
*/}}
{{- define "registry.name" -}}
{{- "registry" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "registry.fullname" -}}
{{- $name := "registry" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
Rabbitmq
Expand the name of the chart.
*/}}
{{- define "rabbitmq.name" -}}
{{- "rabbitmq" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "rabbitmq.fullname" -}}
{{- $name := "rabbitmq" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}


{{/*
global config
*/}}
{{- define "config.global" }}
- name: POLYAXON_DEBUG
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: debug
- name: POLYAXON_CLUSTER_ID
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: cluster-id
- name: POLYAXON_JOB_CONTAINER_NAME
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: job-container-name
- name: POLYAXON_JOB_SIDECAR_CONTAINER_NAME
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: sidecar-container-name
- name: POLYAXON_JOB_SIDECAR_LOG_SLEEP_INTERVAL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: sidecar-log-sleep-interval
- name: POLYAXON_JOB_SIDECAR_PERSIST
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: sidecar-persist
{{- if .Values.k8s.authorisation }}
- name: POLYAXON_K8S_AUTHORISATION
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: k8s-authorisation
{{- end }}
{{- if .Values.k8s.ssl_ca_cert }}
- name: POLYAXON_K8S_SSL_CA_CERT
  value: {{ .Values.k8s.ssl_ca_cert | quote }}
{{- end }}
- name: POLYAXON_K8S_HOST
  value: {{ .Values.k8s.host | quote }}
- name: POLYAXON_K8S_NAMESPACE
  value: {{ .Values.namespace | quote }}
- name: POLYAXON_GPU_NODE_SELECTORS
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: gpu-node-selectors
- name: POLYAXON_ROLE_LABELS_API
  value: {{ .Values.roles.api }}
- name: POLYAXON_ROLE_LABELS_LOG
  value: {{ .Values.roles.log }}
- name: POLYAXON_ROLE_LABELS_WORKER
  value: {{ .Values.roles.worker }}
- name: POLYAXON_ROLE_LABELS_DASHBOARD
  value: {{ .Values.roles.dashboard }}
- name: POLYAXON_TYPE_LABELS_CORE
  value: {{ .Values.types.core }}
- name: POLYAXON_TYPE_LABELS_EXPERIMENT
  value: {{ .Values.types.experiment }}
{{- end -}}

{{/*
versions config
*/}}
{{- define "config.versions" }}
- name: POLYAXON_CLI_MIN_VERSION
  value: {{ .Values.versions.cli.min | quote }}
- name: POLYAXON_CLI_LATEST_VERSION
  value: {{ .Values.versions.cli.latest | quote }}
- name: POLYAXON_PLATFORM_MIN_VERSION
  value: {{ .Values.versions.platform.min | quote }}
- name: POLYAXON_PLATFORM_LATEST_VERSION
  value: {{ .Values.versions.platform.latest | quote }}
- name: POLYAXON_LIB_MIN_VERSION
  value: {{ .Values.versions.lib.min | quote }}
- name: POLYAXON_LIB_LATEST_VERSION
  value: {{ .Values.versions.lib.latest | quote }}
- name: POLYAXON_CHART_VERSION
  value: {{ .Chart.Version | quote }}
{{- end -}}

{{/*
django config
*/}}
{{- define "config.django" }}
- name: POLYAXON_SECRET_KEY
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: polyaxon-secret
- name: POLYAXON_CELERY_ALWAYS_EAGER
  value: {{ .Values.celery.always_eager | quote }}
- name: POLYAXON_CELERYD_PREFETCH_MULTIPLIER
  value: {{ .Values.celery.celeryd_prefetch_multiplier | quote }}
- name: POLYAXON_PASSWORD_LENGTH
  value: {{ default "6" .Values.passwordLength | quote }}
- name: POLYAXON_ADMIN_NAME
  value: {{ .Values.user.name | quote }}
- name: POLYAXON_ADMIN_MAIL
  value: {{ .Values.user.email | quote }}
- name: POLYAXON_EMAIL_FROM
  value: {{ .Values.user.emailFrom | quote }}
- name: POLYAXON_ADMIN_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: user-password
- name: POLYAXON_EMAIL_HOST
  value: {{ .Values.email.host | quote }}
- name: POLYAXON_EMAIL_PORT
  value: {{ .Values.email.port | quote }}
{{- if .Values.email.host_user }}
- name: POLYAXON_EMAIL_HOST_USER
  value: {{ .Values.email.host_user | quote }}
{{- end }}
{{- if .Values.email.host_password }}
- name: POLYAXON_EMAIL_HOST_PASSWORD:
  value: {{ .Values.email.host_password | quote }}
{{- end }}
{{- if .Values.email.backend }}
- name: POLYAXON_EMAIL_BACKEND
  value: {{ .Values.email.backend | quote }}
{{- end }}
{{- end -}}


{{/*
db config
*/}}
{{- define "config.db" }}
- name: POLYAXON_DB_USER
  value: {{ default "polyaxon" .Values.postgresql.postgresUser | quote }}
- name: POLYAXON_DB_NAME
  value: {{ default "polyaxon" .Values.postgresql.postgresDatabase | quote }}
- name: POLYAXON_DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "postgresql.fullname" . }}
      key: postgres-password
- name: POLYAXON_DB_HOST
  value: {{ template "postgresql.fullname" . }}
- name: POLYAXON_DB_PORT
  value: "5432"
{{- end -}}


{{/*
redis config
*/}}
{{- define "config.registry" }}
- name: POLYAXON_REGISTRY_HOST
  value: "localhost:{{ .Values.registry.service.nodePort }}"
{{- end }}

{{/*
redis config
*/}}
{{- define "config.redis" }}
{{- if .Values.redis.usePassword }}
- name: POLYAXON_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "redis.fullname" . }}
      key: redis-password
{{- end }}
- name: POLYAXON_REDIS_HOST
  value: {{ template "redis.fullname" . }}
- name: POLYAXON_REDIS_PORT
  value: "6379"
- name: POLYAXON_REDIS_CELERY_RESULT_BACKEND_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: redis-result-backend-url
- name: POLYAXON_REDIS_JOB_CONTAINERS_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: redis-job-containers-url
- name: POLYAXON_REDIS_TO_STREAM_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: redis-to-stream-url
{{- end }}


{{/*
amqp config
*/}}
{{- define "config.amqp" }}
- name: POLYAXON_AMQP_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}
      key: amqp-url
- name: POLYAXON_RABBITMQ_USER
  value: {{ default "" .Values.rabbitmq.rabbitmqUsername | quote }}
- name: POLYAXON_RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "rabbitmq.fullname" . }}
      key: rabbitmq-password
{{- end -}}


{{/*
Routing keys config
*/}}
{{- define "config.routingKeys" }}
- name: POLYAXON_ROUTING_KEYS_EVENTS_NAMESPACE
  value: {{ .Values.routingKeys.eventsNamespace | quote }}
- name: POLYAXON_ROUTING_KEYS_EVENTS_RESOURCES
  value: {{ .Values.routingKeys.eventsResources | quote }}
- name: POLYAXON_ROUTING_KEYS_EVENTS_JOB_STATUSES
  value: {{ .Values.routingKeys.eventsStatuses | quote }}
- name: POLYAXON_ROUTING_KEYS_LOGS_SIDECARS
  value: {{ .Values.routingKeys.logsSidecars | quote }}
#  other infos
- name: POLYAXON_INTERNAL_EXCHANGE
  value: {{ .Values.exchanges.internal | quote }}
{{- end -}}


{{/*
queues config
*/}}
{{- define "config.queues" }}
- name: POLYAXON_QUEUES_API_EXPERIMENTS
  value: {{ .Values.queues.apiExperiments | quote }}
- name: POLYAXON_QUEUES_API_CLUSTERS
  value: {{ .Values.queues.apiClusters | quote }}
- name: POLYAXON_QUEUES_EVENTS_NAMESPACE
  value: {{ .Values.queues.eventsNamespace | quote }}
- name: POLYAXON_QUEUES_EVENTS_RESOURCES
  value: {{ .Values.queues.eventsResources | quote }}
- name: POLYAXON_QUEUES_EVENTS_JOBS_STATUSES
  value: {{ .Values.queues.eventsStatuses | quote }}
- name: POLYAXON_QUEUES_LOGS_SIDECARS
  value: {{ .Values.queues.logsSidecars | quote }}
- name: POLYAXON_QUEUES_STREAM_EVENTS_NAMESPACE
  value: {{ .Values.queues.streamEventsNamespace | quote }}
- name: POLYAXON_QUEUES_STREAM_EVENTS_RESOURCES
  value: {{ .Values.queues.streamEventsResources | quote }}
- name: POLYAXON_QUEUES_STREAM_EVENTS_JOBS_STATUSES
  value: {{ .Values.queues.streamEventsStatuses | quote }}
- name: POLYAXON_QUEUES_STREAM_LOGS_SIDECARS
  value: {{ .Values.queues.streamLogsSidecars | quote }}
{{- end -}}


{{/*
intervals config
*/}}
{{- define "config.intervals" }}
- name: POLYAXON_INTERVALS_EXPERIMENTS_SCHEDULER
  value: {{ .Values.intervals.experiments_scheduler | quote }}
- name: POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_INFO
  value: {{ .Values.intervals.clusters_update_system_info | quote }}
- name: POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_NODES
  value: {{ .Values.intervals.clusters_update_system_nodes | quote }}
{{- end -}}


{{/*
Config dirs
*/}}
{{- define "config.dirs" }}
- name: POLYAXON_DIRS_UPLOAD
  value: {{ .Values.persistence.upload.mountPath | quote }}
- name: POLYAXON_DIRS_DATA
  value: {{ .Values.persistence.data.mountPath | quote }}
- name: POLYAXON_DIRS_LOGS
  value: {{ .Values.persistence.logs.mountPath | quote }}
- name: POLYAXON_DIRS_OUTPUT
  value: {{ .Values.persistence.outputs.mountPath | quote }}
- name: POLYAXON_DIRS_REPOS
  value: {{ .Values.persistence.repos.mountPath | quote }}
{{- end -}}


{{/*
Volume mounts
*/}}
{{- define "volumes.volumeMounts" }}
- mountPath: {{ .Values.persistence.upload.mountPath }}
  name: {{ template "polyaxon.fullname" . }}-upload
  {{ if .Values.persistence.upload.subPath -}}
  subPath: {{ .Values.persistence.upload.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.data.mountPath }}
  name: {{ template "polyaxon.fullname" . }}-data
  {{ if .Values.persistence.data.subPath -}}
  subPath: {{ .Values.persistence.data.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.logs.mountPath }}
  name: {{ template "polyaxon.fullname" . }}-logs
  {{ if .Values.persistence.logs.subPath -}}
  subPath: {{ .Values.persistence.logs.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.outputs.mountPath }}
  name: {{ template "polyaxon.fullname" . }}-outputs
  {{ if .Values.persistence.outputs.subPath -}}
  subPath: {{ .Values.persistence.outputs.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.repos.mountPath }}
  name: {{ template "polyaxon.fullname" . }}-repos
  {{ if .Values.persistence.repos.subPath -}}
  subPath: {{ .Values.persistence.repos.subPath | quote }}
  {{- end }}
- name: docker
  mountPath: {{ .Values.dirs.docker }}
- name: nvidia
  mountPath: {{ .Values.dirs.nvidia }}
{{- end -}}


{{/*
Volumes
*/}}
{{- define "volumes.volumes" }}
- name: {{ template "polyaxon.fullname" . }}-upload
{{- if .Values.persistence.upload.enabled }}
  persistentVolumeClaim:
    claimName: {{ template "polyaxon.fullname" . }}-upload
{{- else }}
  hostPath:
    path: /tmp/plx/upload
{{ end }}
- name: {{ template "polyaxon.fullname" . }}-repos
{{- if .Values.persistence.repos.enabled }}
  persistentVolumeClaim:
    claimName: {{ template "polyaxon.fullname" . }}-repos
{{- else }}
  hostPath:
    path: /tmp/plx/upload
{{ end }}
- name: {{ template "polyaxon.fullname" . }}-logs
{{- if .Values.persistence.logs.enabled }}
  persistentVolumeClaim:
    claimName: {{ template "polyaxon.fullname" . }}-logs
{{- else }}
  emptyDir: {}
{{ end }}
- name: {{ template "polyaxon.fullname" . }}-data
{{- if .Values.persistence.data.enabled }}
  persistentVolumeClaim:
    claimName: {{ template "polyaxon.fullname" . }}-data
{{- else }}
  emptyDir: {}
{{ end }}
- name: {{ template "polyaxon.fullname" . }}-outputs
{{- if .Values.persistence.outputs.enabled }}
  persistentVolumeClaim:
    claimName: {{ template "polyaxon.fullname" . }}-outputs
{{- else }}
  emptyDir: {}
{{ end }}
- name: docker
  hostPath:
    path: {{ .Values.dirs.docker }}
- name: nvidia
  hostPath:
    path: {{ .Values.dirs.nvidia }}
{{- end -}}

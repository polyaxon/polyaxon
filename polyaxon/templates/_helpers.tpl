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
{{- printf "%s-%s" .Release.Name "polyaxon" | trunc 63 | trimSuffix "-" -}}
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
Create a default fully qualified app names.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}

{{- define "postgresql.fullname" -}}
{{- $name := "postgresql" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "docker-registry.fullname" -}}
{{- $name := "docker-registry" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "redis.fullname" -}}
{{- $name := default "redis" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

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
      name: {{ template "polyaxon.fullname" . }}-config
      key: debug
- name: POLYAXON_CLUSTER_ID
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: cluster-id
- name: POLYAXON_CONTAINER_NAME_JOB
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: container-name-job
- name: POLYAXON_CONTAINER_NAME_SIDECAR
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: container-name-sidecar
- name: POLYAXON_CONTAINER_NAME_PLUGIN_JOB
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: container-name-plugin-job
- name: POLYAXON_JOB_DOCKER_NAME
  value: "{{ .Values.job.image }}:{{ .Values.job.imageTag }}"
- name: POLYAXON_JOB_SIDECAR_DOCKER_IMAGE
  value: "{{ .Values.sidecar.image }}:{{ .Values.sidecar.imageTag }}"
- name: POLYAXON_JOB_DOCKERIZER_IMAGE
  value: "{{ .Values.dockerizer.image }}:{{ .Values.dockerizer.imageTag }}"
- name: POLYAXON_JOB_SIDECAR_LOG_SLEEP_INTERVAL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: sidecar-log-sleep-interval
- name: POLYAXON_JOB_SIDECAR_PERSIST
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: sidecar-persist
- name: POLYAXON_K8S_NODE_NAME
  valueFrom:
    fieldRef:
     fieldPath: spec.nodeName
- name: POLYAXON_K8S_INGRESS_ENABLED
  value: {{ .Values.ingress.enabled | quote }}
- name: POLYAXON_PUBLIC_PLUGIN_JOBS
  value: {{ default false .Values.publicJobs | quote }}
- name: POLYAXON_K8S_INGRESS_ANNOTATIONS
  value: {{ toJson .Values.ingress.annotations | quote }}
- name: POLYAXON_K8S_RBAC_ENABLED
  value: {{ .Values.rbac.enabled | quote }}
- name: POLYAXON_K8S_PROVISIONER_ENABLED
  value: {{ .Values.nfsProvisioner.enabled | quote }}
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
- name: POLYAXON_K8S_APP_NAME
  value: {{ template "polyaxon.fullname" . }}
- name: POLYAXON_K8S_API_HOST
  value: {{ template "polyaxon.fullname" . }}-api
- name: POLYAXON_K8S_API_PORT
  value: {{ .Values.api.service.externalPort | quote }}
- name: POLYAXON_K8S_APP_SECRET_NAME
  value: {{ template "polyaxon.fullname" . }}-secret
- name: POLYAXON_K8S_RABBITMQ_SECRET_NAME
  value: {{ template "rabbitmq.fullname" . }}
- name: POLYAXON_K8S_APP_CONFIG_NAME
  value: {{ template "polyaxon.fullname" . }}-config
- name: POLYAXON_K8S_SERVICE_ACCOUNT_NAME
  value: {{ template "polyaxon.fullname" . }}-serviceaccount
- name: POLYAXON_K8S_GPU_RESOURCE_KEY
{{- if ge .Capabilities.KubeVersion.Minor "8" }}
  value: 'nvidia.com/gpu'
{{- else }}
  value: "alpha.kubernetes.io/nvidia-gpu"
{{- end }}
- name: POLYAXON_ENVIRONMENT
{{- if .Values.environment }}
  value:  {{ .Values.environment | quote }}
{{- else }}
  value: "production"
{{- end }}
- name: POLYAXON_NODE_SELECTORS_CORE
  value: {{ toJson .Values.nodeSelectors.core | quote }}
- name: POLYAXON_NODE_SELECTORS_EXPERIMENTS
  value: {{ toJson .Values.nodeSelectors.experiments | quote }}
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
- name: POLYAXON_APP_LABELS_TENSORBOARD
  value: {{ .Values.apps.tensorboard }}
- name: POLYAXON_APP_LABELS_NOTEBOOK
  value: {{ .Values.apps.notebook }}
- name: POLYAXON_TRACKER_BACKEND
  value: "publisher"
{{- end -}}

{{/*
versions config
*/}}
{{- define "config.versions" }}
- name: POLYAXON_CLI_MIN_VERSION
  value: "0.0.8"
- name: POLYAXON_CLI_LATEST_VERSION
  value: "0.1.0"
- name: POLYAXON_PLATFORM_MIN_VERSION
  value: "0.0.9"
- name: POLYAXON_PLATFORM_LATEST_VERSION
  value: "0.1.0"
- name: POLYAXON_LIB_MIN_VERSION
  value: "0.0.2"
- name: POLYAXON_LIB_LATEST_VERSION
  value: "0.0.5"
- name: POLYAXON_CHART_VERSION
  value: {{ .Chart.Version | quote }}
- name: POLYAXON_CHART_IS_UPGRADE
  value: {{ .Release.IsUpgrade | quote }}
- name: POLYAXON_CHART_REVISION
  value: {{ .Release.Revision | quote }}
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
  value: "false"
- name: POLYAXON_CELERYD_PREFETCH_MULTIPLIER
  value: "4"
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
- name: POLYAXON_DB_CONN_MAX_AGE
  value: "60"
{{- end -}}


{{/*
registry config
*/}}
{{- define "config.registry" }}
- name: POLYAXON_REGISTRY_HOST
  value: {{ template "docker-registry.fullname" . }}
- name: POLYAXON_REGISTRY_PORT
  value: {{ (index .Values "docker-registry").service.port | quote }}
- name: POLYAXON_REGISTRY_NODE_PORT
  value: {{ (index .Values "docker-registry").service.nodePort | quote }}
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
      name: {{ template "polyaxon.fullname" . }}-config
      key: redis-result-backend-url
- name: POLYAXON_REDIS_JOB_CONTAINERS_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: redis-job-containers-url
- name: POLYAXON_REDIS_TO_STREAM_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: redis-to-stream-url
- name: POLYAXON_REDIS_SESSIONS_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: redis-sessions-url
{{- end }}


{{/*
amqp config
*/}}
{{- define "config.amqp" }}
- name: POLYAXON_AMQP_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
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
  value: "events.namespace"
- name: POLYAXON_ROUTING_KEYS_EVENTS_RESOURCES
  value: "events.resources"
- name: POLYAXON_ROUTING_KEYS_EVENTS_JOB_STATUSES
  value: "events.statuses"
- name: POLYAXON_ROUTING_KEYS_LOGS_SIDECARS
  value: "logs.sidecars"
#  other infos
- name: POLYAXON_INTERNAL_EXCHANGE
  value: "internal"
{{- end -}}


{{/*
queues config
*/}}
{{- define "config.queues" }}
- name: POLYAXON_QUEUES_API_EXPERIMENTS
  value: {{ .Values.queues.apiExperiments | quote }}
- name: POLYAXON_QUEUES_API_EXPERIMENTS_SYNC
  value: {{ .Values.queues.apiExperimentsSync | quote }}
- name: POLYAXON_QUEUES_API_CLUSTERS
  value: {{ .Values.queues.apiClusters | quote }}
- name: POLYAXON_QUEUES_API_PIPELINES
  value: {{ .Values.queues.apiPipelines | quote }}
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
- name: POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY
  value: {{ .Values.intervals.operations_max_retry_delay | quote }}
{{- end -}}


{{/*
Config claim_names
*/}}
{{- define "config.claim_names" }}
- name: POLYAXON_CLAIM_NAMES_DATA
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.data.existingClaim }}
  value: {{ .Values.persistence.data.existingClaim | default .Values.persistence.data.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_OUTPUTS
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.data.existingClaim }}
  value: {{ .Values.persistence.outputs.existingClaim | default .Values.persistence.outputs.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_LOGS
  value: {{ .Values.persistence.logs.existingClaim | default .Values.persistence.logs.name }}
- name: POLYAXON_CLAIM_NAMES_UPLOAD
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.upload.existingClaim }}
  value: {{ .Values.persistence.upload.existingClaim | default .Values.persistence.upload.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_REPOS
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.repos.existingClaim }}
  value: {{ .Values.persistence.repos.existingClaim | default .Values.persistence.repos.name }}
{{- else }}
  value: ""
{{- end }}
{{- end -}}

{{/*
Config dirs
*/}}
{{- define "config.dirs" }}
- name: POLYAXON_DIRS_DOCKER
  value: {{ .Values.dirs.docker | quote }}
- name: POLYAXON_DIRS_NVIDIA
  value: {{ toJson .Values.dirs.nvidia | quote }}
{{- if and .Values.mountPaths.nvidia.lib .Values.mountPaths.nvidia.bin .Values.mountPaths.nvidia.libcuda }}
- name: POLYAXON_MOUNT_PATHS_NVIDIA
  value: {{ toJson .Values.mountPaths.nvidia | quote }}
- name: LD_LIBRARY_PATH
  value: "{{ .Values.mountPaths.nvidia.lib }}:{{ .Values.mountPaths.nvidia.libcuda }}"
{{- else if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: POLYAXON_MOUNT_PATHS_NVIDIA
  value: {{ toJson .Values.dirs.nvidia | quote }}
- name: LD_LIBRARY_PATH
  value: "{{ .Values.dirs.nvidia.lib }}:{{ .Values.dirs.nvidia.libcuda }}"
{{- end }}
{{- end -}}

{{/*
Config mount_paths
*/}}
{{- define "config.mount_paths" }}
- name: POLYAXON_MOUNT_PATHS_UPLOAD
  value: {{ .Values.persistence.upload.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_DATA
  value: {{ .Values.persistence.data.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_LOGS
  value: {{ .Values.persistence.logs.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_OUTPUTS
  value: {{ .Values.persistence.outputs.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_REPOS
  value: {{ .Values.persistence.repos.mountPath | quote }}
{{- end -}}

{{/*
Config sub_paths
*/}}
{{- define "config.sub_paths" }}
- name: POLYAXON_SUB_PATHS_UPLOAD
  value: {{ .Values.persistence.upload.subPath | quote }}
- name: POLYAXON_SUB_PATHS_DATA
  value: {{ .Values.persistence.data.subPath | quote }}
- name: POLYAXON_SUB_PATHS_LOGS
  value: {{ .Values.persistence.logs.subPath | quote }}
- name: POLYAXON_SUB_PATHS_OUTPUTS
  value: {{ .Values.persistence.outputs.subPath | quote }}
- name: POLYAXON_SUB_PATHS_REPOS
  value: {{ .Values.persistence.repos.subPath | quote }}
{{- end -}}

{{/*
Auth
*/}}
{{- define "config.auth" }}
{{- if .Values.auth.ldap.enabled }}
- name: POLYAXON_AUTH_LDAP
  value: "true"
- name: POLYAXON_AUTH_LDAP_SERVER_URI
  value: {{ .Values.auth.ldap.serverUri | quote }}
- name: POLYAXON_AUTH_LDAP_GLOBAL_OPTIONS
  value: {{ toJson .Values.auth.ldap.globalOptions | quote }}
- name: POLYAXON_AUTH_LDAP_CONNECTION_OPTIONS
  value: {{ toJson .Values.auth.ldap.connectionOptions | quote }}
- name: POLYAXON_AUTH_LDAP_BIND_DN
  value: {{ .Values.auth.ldap.bindDN | quote }}
- name: POLYAXON_AUTH_LDAP_BIND_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-ldap-bind-password
- name: POLYAXON_AUTH_LDAP_USER_SEARCH_BASE_DN
  value: {{ .Values.auth.ldap.userSearchBaseDN | quote }}
- name: POLYAXON_AUTH_LDAP_USER_SEARCH_FILTERSTR
  value: {{ .Values.auth.ldap.userSearchFilterStr | quote }}
- name: POLYAXON_AUTH_LDAP_USER_DN_TEMPLATE
  value: {{ .Values.auth.ldap.userDNTemplate | quote }}
- name: POLYAXON_AUTH_LDAP_START_TLS
  value: {{ .Values.auth.ldap.startTLS | quote }}
- name: POLYAXON_AUTH_LDAP_USER_ATTR_MAP
  value: {{ toJson .Values.auth.ldap.userAttrMap | quote }}
- name: POLYAXON_AUTH_LDAP_GROUP_SEARCH_BASE_DN
  value: {{ .Values.auth.ldap.groupSearchBaseDN | quote }}
- name: POLYAXON_AUTH_LDAP_GROUP_SEARCH_GROUP_TYPE
  value: {{ .Values.auth.ldap.groupSearchGroupType | quote }}
{{- if .Values.auth.ldap.requireGroup }}
- name: POLYAXON_AUTH_LDAP_REQUIRE_GROUP
  value: {{ .Values.auth.ldap.requireGroup | quote }}
{{- end }}
{{- if .Values.auth.ldap.denyGroup }}
- name: POLYAXON_AUTH_LDAP_DENY_GROUP
  value: {{ .Values.auth.ldap.denyGroup | quote }}
{{- end }}
{{- end }}
{{- if .Values.auth.github.enabled }}
- name: POLYAXON_AUTH_GITHUB
  value: "true"
- name: POLYAXON_AUTH_GITHUB_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-github-client-id
- name: POLYAXON_AUTH_GITHUB_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-github-client-secret
{{- end }}
{{- if .Values.auth.bitbucket.enabled }}
- name: POLYAXON_AUTH_BITBUCKET
  value: "true"
- name: POLYAXON_AUTH_BITBUCKET_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-bitbucket-client-id
- name: POLYAXON_AUTH_BITBUCKET_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-bitbucket-client-secret
{{- end }}
{{- if .Values.auth.gitlab.enabled }}
- name: POLYAXON_AUTH_GITLAB
  value: "true"
- name: POLYAXON_AUTH_GITLAB_URL
  value: {{ .Values.auth.gitlab.url | quote }}
- name: POLYAXON_AUTH_GITLAB_CLIENT_ID
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-gitlab-client-id
- name: POLYAXON_AUTH_GITLAB_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: auth-gitlab-client-secret
{{- end }}
{{- end -}}

{{/*
Config extra_data
*/}}
{{- define "config.extra_data" }}
- name: POLYAXON_EXTRA_PERSISTENCES
  value: {{ toJson .Values.persistence.extra | quote }}
{{- end -}}

{{/*
Volume mounts
*/}}
{{- define "volumes.volumeMounts" }}
- mountPath: {{ .Values.persistence.upload.mountPath }}
  name: upload
  {{ if .Values.persistence.upload.subPath -}}
  subPath: {{ .Values.persistence.upload.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.data.mountPath }}
  name: data
  {{ if .Values.persistence.data.subPath -}}
  subPath: {{ .Values.persistence.data.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.logs.mountPath }}
  name: logs
  {{ if .Values.persistence.logs.subPath -}}
  subPath: {{ .Values.persistence.logs.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.outputs.mountPath }}
  name: outputs
  {{ if .Values.persistence.outputs.subPath -}}
  subPath: {{ .Values.persistence.outputs.subPath | quote }}
  {{- end }}
- mountPath: {{ .Values.persistence.repos.mountPath }}
  name: repos
  {{ if .Values.persistence.repos.subPath -}}
  subPath: {{ .Values.persistence.repos.subPath | quote }}
  {{- end }}
{{- end -}}

{{/*
Dir mounts
*/}}
{{- define "volumes.dirMounts" }}
- name: docker
  mountPath: {{ .Values.mountPaths.docker }}
{{- if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: nvidia-lib
{{- if .Values.mountPaths.nvidia.lib }}
  mountPath: {{ .Values.mountPaths.nvidia.lib | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.lib | quote }}
{{- end }}
- name: nvidia-bin
{{- if .Values.mountPaths.nvidia.bin }}
  mountPath: {{ .Values.mountPaths.nvidia.bin | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.bin | quote }}
{{- end }}
- name: nvidia-libcuda
{{- if .Values.mountPaths.nvidia.libcuda }}
  mountPath: {{ .Values.mountPaths.nvidia.libcuda | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.libcuda | quote }}
{{- end }}
{{- end }}
{{- end -}}


{{/*
Volumes
*/}}
{{- define "volumes.volumes" }}
- name: upload
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.upload.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.upload.existingClaim | default .Values.persistence.upload.name }}
{{- else }}
  hostPath:
    path:  {{ .Values.persistence.upload.mountPath }}
{{ end }}
- name: repos
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.repos.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.repos.existingClaim | default .Values.persistence.repos.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.repos.mountPath }}
{{ end }}
- name: logs
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.logs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.logs.existingClaim | default .Values.persistence.logs.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.logs.mountPath }}
{{ end }}
- name: data
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.data.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.data.existingClaim | default .Values.persistence.data.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.data.mountPath }}
{{ end }}
- name: outputs
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.outputs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.outputs.existingClaim | default .Values.persistence.outputs.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.outputs.mountPath }}
{{ end }}
{{- end -}}


{{/*
Dirs
*/}}
{{- define "volumes.dirs" }}
- name: docker
  hostPath:
    path: {{ .Values.dirs.docker | quote }}
{{- if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: nvidia-lib
  hostPath:
    path: {{ .Values.dirs.nvidia.lib | quote }}
- name: nvidia-bin
  hostPath:
    path: {{ .Values.dirs.nvidia.bin | quote }}
- name: nvidia-libcuda
  hostPath:
    path: {{ .Values.dirs.nvidia.libcuda | quote }}
{{- end }}
{{- end -}}

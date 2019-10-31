{{- /*
scheduler celery config
*/}}
{{- define "config.celery.scheduler" -}}
{{- if .Values.scheduler.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.scheduler.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.scheduler.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.scheduler.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.scheduler.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.scheduler.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.scheduler.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.scheduler.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.scheduler.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.scheduler.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.scheduler.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.scheduler.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.scheduler.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.scheduler.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}


{{- /*
hpsearch celery config
*/}}
{{- define "config.celery.hpsearch" -}}
{{- if .Values.hpsearch.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.hpsearch.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.hpsearch.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.hpsearch.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.hpsearch.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.hpsearch.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.hpsearch.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.hpsearch.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.hpsearch.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}


{{- /*
eventsHandlers celery config
*/}}
{{- define "config.celery.eventsHandlers" -}}
{{- if .Values.eventsHandlers.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.eventsHandlers.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.eventsHandlers.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.eventsHandlers.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.eventsHandlers.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.eventsHandlers.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.eventsHandlers.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.eventsHandlers.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.eventsHandlers.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}

{{- /*
k8sEventsHandlers celery config
*/}}
{{- define "config.celery.k8sEventsHandlers" -}}
{{- if .Values.k8sEventsHandlers.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.k8sEventsHandlers.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.k8sEventsHandlers.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.k8sEventsHandlers.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.k8sEventsHandlers.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.k8sEventsHandlers.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.k8sEventsHandlers.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.k8sEventsHandlers.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.k8sEventsHandlers.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}

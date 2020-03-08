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

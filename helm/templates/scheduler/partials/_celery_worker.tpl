{{- /*
Worker celery config
*/}}
{{- define "config.celery.worker" -}}
{{- if .Values.worker.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.worker.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.worker.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.worker.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.worker.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.worker.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.worker.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.worker.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.worker.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.worker.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.worker.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.worker.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.worker.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.worker.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}

{{- /*
Compiler celery config
*/}}
{{- define "config.celery.compiler" -}}
{{- if .Values.compiler.celery.taskTrackStarted }}
- name: POLYAXON_CELERY_TASK_TRACK_STARTED
  value: {{ .Values.compiler.celery.taskTrackStarted | quote }}
{{- end }}
{{- if .Values.compiler.celery.brokerPoolLimit }}
- name: POLYAXON_CELERY_BROKER_POOL_LIMIT
  value: {{ .Values.compiler.celery.brokerPoolLimit | quote }}
{{- end }}
{{- if .Values.compiler.celery.confirmPublish }}
- name: POLYAXON_CELERY_CONFIRM_PUBLISH
  value: {{ .Values.compiler.celery.confirmPublish | quote }}
{{- end }}
{{- if .Values.compiler.celery.workerPrefetchMultiplier }}
- name: POLYAXON_CELERY_WORKER_PREFETCH_MULTIPLIER
  value: {{ .Values.compiler.celery.workerPrefetchMultiplier | quote }}
{{- end }}
{{- if .Values.compiler.celery.workerMaxTasksPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_TASKS_PER_CHILD
  value: {{ .Values.compiler.celery.workerMaxTasksPerChild | quote }}
{{- end }}
{{- if .Values.compiler.celery.workerMaxMemoryPerChild }}
- name: POLYAXON_CELERY_WORKER_MAX_MEMORY_PER_CHILD
  value: {{ .Values.compiler.celery.workerMaxMemoryPerChild | quote }}
{{- end }}
{{- if .Values.compiler.celery.taskAlwaysEager }}
- name: POLYAXON_CELERY_TASK_ALWAYS_EAGER
  value: {{ .Values.compiler.celery.taskAlwaysEager | quote }}
{{- end }}
{{- end -}}

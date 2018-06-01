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

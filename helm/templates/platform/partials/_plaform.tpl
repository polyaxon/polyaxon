{{- /*
Secret envFrom
*/}}
{{- define "config.envFrom.secret" -}}
{{- if .Values.platformSecret }}
- secretRef:
    name: {{ .Values.platformSecret }}
{{- else }}
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-secret
{{- if .Values.encryptionSecret }}
- secretRef:
    name: {{ .Values.encryptionSecret }}
{{- end }}
{{- end }}
{{- end -}}

{{- /*
Platform envFrom
*/}}
{{- define "config.envFrom.platform" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-platform-config
{{- if (not .Values.organizationKey) }}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-agent-config
{{- end }}
{{- end -}}

{{- /*
secrets config
*/}}
{{- define "config.envs" -}}
{{- if not .Values.platformSecret }}
{{- if (index .Values "rabbitmq-ha").enabled }}
- name: POLYAXON_RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "rabbitmq.fullname" . }}
      key: rabbitmq-password
{{- end }}
{{- if and (not (index .Values "rabbitmq-ha").enabled) .Values.scheduler.enabled (eq .Values.broker "rabbitmq") }}
- name: POLYAXON_RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-rabbitmq-secret
      key: rabbitmq-password
{{- end }}
{{- if and .Values.redis.enabled .Values.redis.usePassword }}
- name: POLYAXON_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "redis.fullname" . }}
      key: redis-password
{{- end }}
{{- if and (not .Values.redis.enabled) .Values.externalServices.redis.usePassword }}
- name: POLYAXON_REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-redis-secret
      key: redis-password
{{- end }}
- name: POLYAXON_DB_PASSWORD
  valueFrom:
    secretKeyRef:
{{- if .Values.postgresql.enabled }}
      name: {{ template "pgsql.fullname" . }}
{{- else }}
      name: {{ template "polyaxon.fullname" . }}-postgresql-secret
{{- end }}
      key: postgresql-password
{{- end }}
{{- end -}}

{{- /*
Platform checksum
*/}}
{{- define "config.checksum.platform" -}}
checksum/common-config: {{ include (print $.Template.BasePath "/common-cm.yaml") . | sha256sum }}
checksum/platform-config: {{ include (print $.Template.BasePath "/platform-cm.yaml") . | sha256sum }}
{{- if (not .Values.secret) }}
checksum/agent-secrets: {{ include (print $.Template.BasePath "/agent-secrets.yaml") . | sha256sum }}
{{- end }}
{{- end -}}

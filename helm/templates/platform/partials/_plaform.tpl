{{- /*
Secret envFrom
*/}}
{{- define "config.envFrom.secret" -}}
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-secret
{{- if .Values.encryptionSecret }}
- secretRef:
    name: {{ .Values.encryptionSecret }}
{{- end }}
{{- end -}}

{{- /*
Platform envFrom
*/}}
{{- define "config.envFrom.platform" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-platform-config
{{- if (not .Values.organizationKey) }}
    name: {{ template "polyaxon.fullname" . }}-agent-config
{{- end }}
{{- end -}}

{{- /*
secrets config
*/}}
{{- define "config.envs" -}}
- name: POLYAXON_RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
{{- if (index .Values "rabbitmq-ha").enabled }}
      name: {{ template "rabbitmq.fullname" . }}
{{- else }}
      name: {{ template "polyaxon.fullname" . }}-rabbitmq-secret
{{- end }}
      key: rabbitmq-password
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
{{- end -}}

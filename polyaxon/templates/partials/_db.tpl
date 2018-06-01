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

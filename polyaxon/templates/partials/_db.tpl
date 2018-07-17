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
{{ if .Values.postgresql.enabled }}
      name: {{ template "postgresql.fullname" . }}
{{ else }}
      name: {{ template "polyaxon.fullname" . }}-postgres-secret
{{- end}}
      key: postgres-password
- name: POLYAXON_DB_HOST
{{ if .Values.postgresql.enabled }}
  value: {{  template "postgresql.fullname" . }}
{{ else }}
  value: {{ .Values.postgresql.externalPostgresHost | quote }}
{{ end }}
- name: POLYAXON_DB_PORT
  value: "5432"
- name: POLYAXON_DB_CONN_MAX_AGE
  value: "60"
{{- end -}}

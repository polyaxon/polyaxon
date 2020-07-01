{{- /*
Config labels apps api
*/}}
{{- define "config.labels.apps.api" -}}
app.kubernetes.io/name: {{ template "polyaxon.fullname" . }}-api
{{- end -}}

{{- /*
Config labels apps pgbouncer
*/}}
{{- define "config.labels.apps.pgbouncer" -}}
app.kubernetes.io/name: {{ template "polyaxon.fullname" . }}-pgbouncer
{{- end -}}

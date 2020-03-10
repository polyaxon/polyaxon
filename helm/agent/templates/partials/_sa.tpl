{{- /*
service account
*/}}
{{- define "config.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-sa
{{- end }}
{{- end -}}

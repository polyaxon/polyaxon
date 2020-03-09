{{- /*
service account
*/}}
{{- define "config.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-serviceaccount
{{- end }}
{{- end -}}

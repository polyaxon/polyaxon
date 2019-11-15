{{- /*
service account
*/}}
{{- define "config.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: polyaxon-agent-sa
{{- end }}
{{- end -}}

{{- /*
Operator service account
*/}}
{{- define "config.operator.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-operator-sa
{{- end }}
{{- end -}}

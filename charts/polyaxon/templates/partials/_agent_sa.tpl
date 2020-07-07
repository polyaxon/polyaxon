{{- /*
service account
*/}}
{{- define "config.agent.sa" -}}
{{- if and .Values.rbac.enabled (or .Values.agent.enabled (not .Values.organizationKey)) }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-agent-sa
{{- end }}
{{- end -}}

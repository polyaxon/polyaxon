{{- /*
Runs service account
*/}}
{{- define "config.runs.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-runs-sa
{{- end }}
{{- end -}}

{{- /*
Operator service account
*/}}
{{- define "config.operator.sa" -}}
{{- if .Values.rbac.enabled }}
serviceAccountName: {{ template "polyaxon.fullname" . }}-operator-sa
{{- end }}
{{- end -}}

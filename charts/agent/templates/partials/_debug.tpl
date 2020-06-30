{{- /*
debug mode config
*/}}
{{- define "config.debugMode" -}}
{{- if .Values.debugMode }}
- name: POLYAXON_DEBUG
  value: "true"
{{- end }}
{{- end -}}

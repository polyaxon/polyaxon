{{- /*
Metrics/Stats Backend
*/}}
{{- define "config.metrics" -}}
{{- if .Values.metrics.enabled }}
{"host": "{{ template "polyaxon.fullname" . }}-metrics","port": 9125}
{{- end }}
{{- end -}}

{{- define "api.host" -}}
{{- template "polyaxon.fullname" . }}-gateway
{{- end -}}

{{- define "api.port" -}}
{{- default 80 .Values.gateway.service.port -}}
{{- end -}}

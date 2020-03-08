{{- define "api.host" -}}
{{- if .Values.api.enabled }}
{{- template "polyaxon.fullname" . }}-api
{{- else }}
{{- .Values.externalServices.api.host }}
{{- end }}
{{- end -}}

{{- define "api.port" -}}
{{- if .Values.api.enabled }}
{{- default 80 .Values.api.service.port -}}
{{- else }}
{{- default 443 .Values.externalServices.api.port }}
{{- end }}
{{- end -}}

{{- define "streams.host" -}}
{{- template "polyaxon.fullname" . }}-streams
{{- end -}}

{{- define "streams.port" -}}
{{- default 80 .Values.streams.service.port -}}
{{- end -}}

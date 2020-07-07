{{- /*
Proxies envFrom
*/}}
{{- define "config.envFrom.proxies" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-proxies-config
{{- end -}}

{{- /*
Proxies apis
*/}}
{{- define "proxies.api.host" -}}
{{- if .Values.api.enabled }}
{{- template "polyaxon.fullname" . }}-api
{{- else }}
{{- .Values.externalServices.api.host }}
{{- end }}
{{- end -}}

{{- define "proxies.api.port" -}}
{{- if .Values.api.enabled }}
{{- default 80 .Values.api.service.port -}}
{{- else }}
{{- default 443 .Values.externalServices.api.port }}
{{- end }}
{{- end -}}

{{- define "proxies.api.useResolver" -}}
{{- if .Values.api.enabled }}
{{- default "false" .Values.api.useResolver -}}
{{- else }}
{{- default "false" .Values.externalServices.api.useResolver -}}
{{- end }}
{{- end -}}

{{- define "proxies.streams.host" -}}
{{- template "polyaxon.fullname" . }}-streams
{{- end -}}

{{- define "proxies.streams.port" -}}
{{- default 80 .Values.streams.service.port -}}
{{- end -}}

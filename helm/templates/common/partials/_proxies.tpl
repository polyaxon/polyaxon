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
{{- define "gateway.host" -}}
{{- if .Values.gateway.enabled }}
{{- template "polyaxon.fullname" . }}-gateway
{{- else if .Values.externalServices.gateway.host }}
{{- .Values.externalServices.gateway.host }}
{{- else }}
{{- printf "localhost" -}}
{{- end }}
{{- end -}}

{{- define "gateway.port" -}}
{{- if .Values.gateway.enabled }}
{{- default 80 .Values.gateway.service.port -}}
{{- else if .Values.externalServices.gateway.port }}
{{- default 443 .Values.externalServices.gateway.port }}
{{- else }}
{{- printf "80" -}}
{{- end }}
{{- end -}}

{{- define "gateway.scheme" -}}
{{- if .Values.gateway.enabled }}
{{- printf "http" -}}
{{- else if eq .Values.externalServices.gateway.port 443 }}
{{- printf "https" -}}
{{- else }}
{{- printf "http" -}}
{{- end }}
{{- end -}}

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

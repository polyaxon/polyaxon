{{- /*
Ingress
*/}}
{{- define "config.ingres.backend" -}}
backend:
{{- if eq .Values.ingress.backend "api" }}
  serviceName: {{ template "polyaxon.fullname" . }}-api
  servicePort: {{ .Values.api.service.port }}
{{- else }}
  serviceName: {{ template "polyaxon.fullname" . }}-gateway
  servicePort: {{ .Values.gateway.service.port }}
{{- end }}
{{- end -}}

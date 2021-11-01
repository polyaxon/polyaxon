{{- /*
Ingress
*/}}
{{- define "config.ingress.backend" -}}
pathType: {{ default "Prefix" .Values.ingress.pathType }}
backend:
{{- if eq .Values.ingress.backend "api" }}
  service:
    name: {{ template "polyaxon.fullname" . }}-api
    port:
      number: {{ .Values.api.service.port }}
{{- else }}
  service:
    name: {{ template "polyaxon.fullname" . }}-gateway
    port:
      number: {{ .Values.gateway.service.port }}
{{- end }}
{{- end -}}

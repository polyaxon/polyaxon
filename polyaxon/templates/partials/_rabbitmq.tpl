{{- define "rabbitmq.fullname" -}}
{{- $name := "rabbitmq-ha" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "rabbitmq.host" -}}
{{- if (index .Values "rabbitmq-ha").enabled }}
{{- template "rabbitmq.fullname" . }}
{{- else }}
{{- (index .Values "rabbitmq-ha").externalRabbitmqHost }}
{{- end }}
{{- end -}}

{{- define "rabbitmq.port" -}}
{{- default 5672 (index .Values "rabbitmq-ha").port -}}
{{- end -}}

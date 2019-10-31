{{- define "rabbitmq.fullname" -}}
{{- $name := "rabbitmq-ha" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "rabbitmq.host" -}}
{{- if (index .Values "rabbitmq-ha").enabled }}
{{- template "rabbitmq.fullname" . }}
{{- else }}
{{- .Values.externalServices.rabbitmq.host }}
{{- end }}
{{- end -}}

{{- define "rabbitmq.port" -}}
{{- if (index .Values "rabbitmq-ha").enabled }}
{{- default 5672 (index .Values "rabbitmq-ha").port -}}
{{- else }}
{{- default 5672 .Values.externalServices.rabbitmq.port }}
{{- end }}
{{- end -}}

{{- define "rabbitmq.user" -}}
{{- if (index .Values "rabbitmq-ha").enabled }}
{{- default "" (index .Values "rabbitmq-ha").rabbitmqUsername -}}
{{- else }}
{{- default "" .Values.externalServices.rabbitmq.user }}
{{- end }}
{{- end -}}

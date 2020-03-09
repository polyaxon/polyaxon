{{- define "redis.fullname" -}}
{{- $name := default "redis" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "redis.host" -}}
{{- if .Values.redis.enabled }}
{{- template "redis.fullname" . }}-master
{{- else }}
{{- .Values.externalServices.redis.host }}
{{- end }}
{{- end -}}

{{- define "redis.port" -}}
{{- if .Values.redis.enabled }}
{{- default 6379 .Values.redis.port -}}
{{- else }}
{{- default 6379 .Values.externalServices.redis.port }}
{{- end }}
{{- end -}}

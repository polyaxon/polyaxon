{{- define "redis.fullname" -}}
{{- $name := default "redis" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "redis.host" -}}
{{- if .Values.redis.enabled }}
{{- template "redis.fullname" . }}-master
{{- else }}
{{- .Values.redis.externalRedisHost }}
{{- end }}
{{- end -}}

{{- define "redis.port" -}}
{{- default 6379 .Values.redis.port -}}
{{- end -}}

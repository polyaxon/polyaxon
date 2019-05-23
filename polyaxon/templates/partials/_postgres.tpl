{{- define "postgresql.fullname" -}}
{{- $name := "postgresql" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "postgresql.host" -}}
{{- if .Values.postgresql.enabled }}
{{- template "postgresql.fullname" . }}
{{- else }}
{{- .Values.postgresql.externalPostgresHost }}
{{- end }}
{{- end -}}

{{- define "postgresql.port" -}}
{{- default 5432 .Values.postgresql.port -}}
{{- end -}}

{{- define "postgresql.fullname" -}}
{{- $name := "postgresql" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "postgresql.host" -}}
{{- if .Values.postgresql.enabled }}
{{- template "postgresql.fullname" . }}
{{- else }}
{{- .Values.externalServices.postgresql.host }}
{{- end }}
{{- end -}}

{{- define "postgresql.port" -}}
{{- if .Values.postgresql.enabled }}
{{- default 5432 .Values.postgresql.port -}}
{{- else }}
{{- default 5432 .Values.externalServices.postgresql.port }}
{{- end }}
{{- end -}}

{{- define "postgresql.user" -}}
{{- if .Values.postgresql.enabled }}
{{- default "polyaxon" .Values.postgresql.postgresUser -}}
{{- else }}
{{- default "polyaxon" .Values.externalServices.postgresql.user }}
{{- end }}
{{- end -}}

{{- define "postgresql.database" -}}
{{- if .Values.postgresql.enabled }}
{{- default "polyaxon" .Values.postgresql.postgresDatabase -}}
{{- else }}
{{- default "polyaxon" .Values.externalServices.postgresql.database }}
{{- end }}
{{- end -}}


{{- define "postgresql.connMaxAge" -}}
{{- if .Values.postgresql.enabled }}
{{- default "polyaxon" .Values.postgresql.connMaxAge -}}
{{- else }}
{{- .Values.externalServices.postgresql.connMaxAge }}
{{- end }}
{{- end -}}

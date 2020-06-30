{{- define "pgsql.fullname" -}}
{{- $name := "postgresql" -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "pgsql.host" -}}
{{- if .Values.postgresql.enabled -}}
{{- template "pgsql.fullname" . }}
{{- else }}
{{- .Values.externalServices.postgresql.host }}
{{- end }}
{{- end -}}

{{- define "pgsql.port" -}}
{{- if .Values.postgresql.enabled -}}
{{- default 5432 .Values.postgresql.service.port -}}
{{- else }}
{{- default 5432 .Values.externalServices.postgresql.port }}
{{- end }}
{{- end -}}

{{- define "pgsql.user" -}}
{{- if .Values.postgresql.enabled -}}
{{- default "polyaxon" .Values.postgresql.postgresqlUsername -}}
{{- else }}
{{- default "polyaxon" .Values.externalServices.postgresql.user }}
{{- end }}
{{- end -}}

{{- define "pgsql.database" -}}
{{- if .Values.postgresql.enabled -}}
{{- default "polyaxon" .Values.postgresql.postgresqlDatabase -}}
{{- else }}
{{- default "polyaxon" .Values.externalServices.postgresql.database }}
{{- end }}
{{- end -}}


{{- define "pgsql.connMaxAge" -}}
{{- if .Values.postgresql.enabled -}}
{{- default "polyaxon" .Values.postgresql.connMaxAge -}}
{{- else }}
{{- .Values.externalServices.postgresql.connMaxAge }}
{{- end }}
{{- end -}}

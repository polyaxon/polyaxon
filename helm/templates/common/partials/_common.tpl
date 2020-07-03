{{- /*
Secret platformSecret
*/}}
{{- define "config.platformSecret" -}}
{{- if .Values.platformSecret }}
{{- .Values.platformSecret | quote }}
{{- else }}
{{- template "polyaxon.fullname" . }}-platform-secret
{{- end }}
{{- end -}}

{{- /*
Common envFrom
*/}}
{{- define "config.envFrom.common" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-config
{{- end -}}

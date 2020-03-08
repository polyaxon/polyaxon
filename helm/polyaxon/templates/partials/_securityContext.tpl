{{- /*
Config securityContext with static GID
*/}}
{{- define "securityContext" -}}
{{- if .Values.securityContext.enabled }}
securityContext:
  fsGroup: {{ .Values.securityContext.group }}
{{- end }}
{{- end -}}

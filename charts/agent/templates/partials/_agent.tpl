{{- /*
Agent envFrom
*/}}
{{- define "config.envFrom.agent" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-agent-config
{{- if .Values.agent.token }}
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-agent-secret
{{- end }}
{{- end -}}

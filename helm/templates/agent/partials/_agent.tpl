{{- /*
Agent envFrom
*/}}
{{- define "config.envFrom.agent" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-agent-config
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-agent-secret
{{- end -}}

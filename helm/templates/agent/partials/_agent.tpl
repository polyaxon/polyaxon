{{- /*
Agent envFrom
*/}}
{{- define "config.envFrom.agent" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-agent-config
{{- if .Values.agentSecret }}
- secretRef:
    name: {{ .Values.agentSecret }}
{{- else if .Values.agent.token }}
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-agent-secret
{{- end }}
{{- end -}}

{{- /*
Agent checksum
*/}}
{{- define "config.checksum.agent" -}}
checksum/common-config: {{ include (print $.Template.BasePath "/common-cm.yaml") . | sha256sum }}
checksum/agent-config: {{ include (print $.Template.BasePath "/agent-cm.yaml") . | sha256sum }}
checksum/proxies-config: {{ include (print $.Template.BasePath "/proxies-cm.yaml") . | sha256sum }}
{{- if (not .Values.secret) }}
checksum/agent-secrets: {{ include (print $.Template.BasePath "/agent-secrets.yaml") . | sha256sum }}
{{- end }}
{{- end -}}

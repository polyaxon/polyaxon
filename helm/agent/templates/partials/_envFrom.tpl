{{- /*
Config envFrom
*/}}
{{- define "config.envFrom" -}}
- configMapRef:
    name: polyaxon-agent-config
- secretRef:
    name: polyaxon-agent-secret
{{- end -}}

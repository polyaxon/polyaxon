{{- /*
Proxies envFrom
*/}}
{{- define "config.envFrom.proxies" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-proxies-config
{{- end -}}

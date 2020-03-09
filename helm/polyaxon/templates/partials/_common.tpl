{{- /*
Common envFrom
*/}}
{{- define "config.envFrom.common" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-config
{{- end -}}

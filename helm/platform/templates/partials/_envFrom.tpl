{{- /*
Config envFrom
*/}}
{{- define "config.envFrom" -}}
- configMapRef:
    name: {{ template "polyaxon.fullname" . }}-config
- secretRef:
    name: {{ template "polyaxon.fullname" . }}-secret
{{- if .Values.encryptionSecret }}
- secretRef:
    name: {{ .Values.encryptionSecret }}
{{- end }}
{{- end -}}

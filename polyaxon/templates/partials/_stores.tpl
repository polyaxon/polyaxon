{{- /*
Config outputs stores secrets
*/}}
{{- define "config.storesSecrets.outputs" -}}
{{- if .Values.persistence.outputs }}
{{- range $key, $val := .Values.persistence.outputs }}
{{- if $val.store }}
- name: {{ $val.secretKey | quote }}
  valueFrom:
    secretKeyRef:
      name: {{ $val.secret | quote }}
      key: {{ $val.secretKey | quote }}
{{- end }} {{- /* end store check */ -}}
{{- end}}  {{- /* end range */ -}}
{{- end }} {{- /* end persistence check */ -}}
{{- end -}}

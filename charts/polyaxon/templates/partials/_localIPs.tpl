{{- /*
local IP hosts config
*/}}
{{- define "config.hostIps" -}}
{{- if .Values.includeHostIps }}
- name: POLYAXON_POD_IP
  valueFrom:
    fieldRef:
      fieldPath: status.podIP
- name: POLYAXON_HOST_IP
  valueFrom:
    fieldRef:
      fieldPath: status.hostIP
{{- end }}
{{- end -}}

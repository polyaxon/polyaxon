{{- /*
dns config
*/}}
{{- define "config.dns" -}}
{{- if .Values.dns.backend }}
- name: POLYAXON_DNS_BACKEND
  value: {{ .Values.dns.backend | quote }}
{{- end }}
{{- if .Values.dns.customCluster }}
- name: POLYAXON_DNS_CUSTOM_CLUSTER
  value: {{ .Values.dns.customCluster | quote }}
{{- end }}
{{- if .Values.dns.POLYAXON_DNS_PREFIX }}
- name: POLYAXON_DNS_PREFIX
  value: {{ .Values.dns.prefix | quote }}
{{- end }}
{{- end -}}

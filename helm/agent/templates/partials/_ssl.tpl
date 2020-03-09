{{- /*
SSL volume mount
*/}}
{{- define "ssl.mount" -}}
{{- if and .Values.ssl.enabled .Values.ssl.secretName }}
- name: polyaxon-ssl-volume
  readOnly: true
  mountPath: {{ default "/etc/ssl" .Values.ssl.path | quote }}
{{- end }}
{{- end -}}  {{- /* end def ssl volume mounts */ -}}

{{- /*
SSL Volume
*/}}
{{- define "ssl.volume" -}}
{{- if and .Values.ssl.enabled .Values.ssl.secretName }}
- name: polyaxon-ssl-volume
  secret:
    secretName: {{ .Values.ssl.secretName | quote }}
{{- end }}
{{- end -}}  {{- /* end def ssl volume mounts */ -}}

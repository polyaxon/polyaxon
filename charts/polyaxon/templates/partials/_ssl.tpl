{{- /*
SSL volume mount
*/}}
{{- define "ssl.mount" -}}
{{- if and .Values.ssl.enabled .Values.ssl.secretName }}
- name: polyaxon-ssl-volume
  readOnly: true
  mountPath: {{ .Values.ssl.path | default "/etc/ssl" | quote }}
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

{{- /*
SSL Enabled
*/}}
{{- define "ssl.enabled" -}}
{{- if or (and .Values.ssl.enabled .Values.ssl.secretName) .Values.ingress.tls }}
{{- printf "true" -}}
{{- else }}
{{- printf "false" -}}
{{- end }}
{{- end -}}  {{- /* end def ssl volume mounts */ -}}

{{- /*
SSL redirect enabled
*/}}
{{- define "ssl.redirect.enabled" -}}
{{- if and .Values.ssl.enabled .Values.ssl.secretName }}
{{- printf "true" -}}
{{- else }}
{{- printf "false" -}}
{{- end }}
{{- end -}}  {{- /* end def ssl volume mounts */ -}}

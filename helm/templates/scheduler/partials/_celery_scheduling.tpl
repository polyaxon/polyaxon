{{- /*
Config celery scheduling
*/}}
{{- define "config.celeryScheduling" -}}
{{- if .Values.celeryNodeSelector }}
nodeSelector:
{{ toYaml .Values.celeryNodeSelector | indent 2}}
{{- else }}
{{- if .Values.nodeSelector }}
nodeSelector:
{{ toYaml .Values.nodeSelector | indent 2}}
{{- end }}
{{- end }}
{{- if .Values.celeryAffinity }}
affinity:
{{ toYaml .Values.celeryAffinity | indent 2 }}
{{- else }}
{{- if .Values.affinity }}
affinity:
{{ toYaml .Values.affinity | indent 2 }}
{{- end }}
{{- end }}
{{- if .Values.celeryTolerations }}
tolerations:
{{ toYaml .Values.celeryTolerations | indent 2 }}
{{- else }}
{{- if .Values.tolerations }}
tolerations:
{{ toYaml .Values.tolerations | indent 2 }}
{{- end }}
{{- end }}
{{- end -}}

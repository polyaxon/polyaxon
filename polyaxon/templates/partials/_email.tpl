{{/*
Config emails
*/}}
{{- define "config.emails" }}
{{- if .Values.email.from }}
- name: POLYAXON_EMAIL_FROM
  value: {{ .Values.email.from | quote }}
{{- end }}
{{- if .Values.email.subjectPrefix }}
- name: POLYAXON_EMAIL_SUBJECT_PREFIX
  value: {{ .Values.email.subjectPrefix | quote }}
{{- end }}
- name: POLYAXON_EMAIL_HOST
  value: {{ .Values.email.host | quote }}
- name: POLYAXON_EMAIL_PORT
  value: {{ .Values.email.port | quote }}
- name: POLYAXON_EMAIL_USE_TLS
  value: {{ .Values.email.useTls | quote }}
{{- if .Values.email.hostUser }}
- name: POLYAXON_EMAIL_HOST_USER
  value: {{ .Values.email.hostUser | quote }}
{{- end }}
{{- if .Values.email.hostPassword }}
- name: POLYAXON_EMAIL_HOST_PASSWORD:
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: email-host-password
{{- end }}
{{- if .Values.email.backend }}
- name: POLYAXON_EMAIL_BACKEND
  value: {{ .Values.email.backend | quote }}
{{- end }}
{{- end -}}

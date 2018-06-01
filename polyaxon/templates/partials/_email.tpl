{{/*
Config dirs
*/}}
{{- define "config.emails" }}
- name: POLYAXON_ADMIN_NAME
  value: {{ .Values.user.name | quote }}
- name: POLYAXON_ADMIN_MAIL
  value: {{ .Values.user.email | quote }}
- name: POLYAXON_EMAIL_FROM
  value: {{ .Values.user.emailFrom | quote }}
- name: POLYAXON_ADMIN_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: user-password
- name: POLYAXON_EMAIL_HOST
  value: {{ .Values.email.host | quote }}
- name: POLYAXON_EMAIL_PORT
  value: {{ .Values.email.port | quote }}
{{- if .Values.email.host_user }}
- name: POLYAXON_EMAIL_HOST_USER
  value: {{ .Values.email.host_user | quote }}
{{- end }}
{{- if .Values.email.host_password }}
- name: POLYAXON_EMAIL_HOST_PASSWORD:
  value: {{ .Values.email.host_password | quote }}
{{- end }}
{{- if .Values.email.backend }}
- name: POLYAXON_EMAIL_BACKEND
  value: {{ .Values.email.backend | quote }}
{{- end }}
{{- end -}}

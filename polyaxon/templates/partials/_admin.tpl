{{/*
Config admin
*/}}
{{- define "config.admin" }}
- name: POLYAXON_ADMIN_NAME
  value: {{ .Values.user.username | quote }}
- name: POLYAXON_ADMIN_MAIL
  value: {{ .Values.user.email | quote }}
- name: POLYAXON_ADMIN_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "polyaxon.fullname" . }}-secret
      key: user-password
{{- end -}}

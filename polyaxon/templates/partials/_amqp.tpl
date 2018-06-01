{{/*
amqp config
*/}}
{{- define "config.amqp" }}
- name: POLYAXON_AMQP_URL
  valueFrom:
    configMapKeyRef:
      name: {{ template "polyaxon.fullname" . }}-config
      key: amqp-url
- name: POLYAXON_RABBITMQ_USER
  value: {{ default "" .Values.rabbitmq.rabbitmqUsername | quote }}
- name: POLYAXON_RABBITMQ_PASSWORD
  valueFrom:
    secretKeyRef:
      name: {{ template "rabbitmq.fullname" . }}
      key: rabbitmq-password
- name: POLYAXON_INTERNAL_EXCHANGE
  value: "internal"
{{- end -}}

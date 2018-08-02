{{/*
Config integrations
*/}}
{{- define "config.integrations" }}
{{- if .Values.integrations.slack }}
- name: POLYAXON_INTEGRATIONS_SLACK_WEBHOOKS
  value: {{ toJson .Values.integrations.slack | quote }}
{{- end }}
{{- if .Values.integrations.hipchat }}
- name: POLYAXON_INTEGRATIONS_HIPCHAT_WEBHOOKS
  value: {{ toJson .Values.integrations.hipchat | quote }}
{{- end }}
{{- if .Values.integrations.mattermost }}
- name: POLYAXON_INTEGRATIONS_HIPCHAT_WEBHOOKS
  value: {{ toJson .Values.integrations.mattermost | quote }}
{{- end }}
{{- if .Values.integrations.discord }}
- name: POLYAXON_INTEGRATIONS_DISCORD_WEBHOOKS
  value: {{ toJson .Values.integrations.discord | quote }}
{{- end }}
{{- if .Values.integrations.pagerduty }}
- name: POLYAXON_INTEGRATIONS_PAGER_DUTY_WEBHOOKS
  value: {{ toJson .Values.integrations.pagerduty | quote }}
{{- end }}
{{- if .Values.integrations.webhooks }}
- name: POLYAXON_INTEGRATIONS_WEBHOOKS
  value: {{ toJson .Values.integrations.webhooks | quote }}
{{- end }}
{{- end -}}

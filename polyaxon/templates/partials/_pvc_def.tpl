{{- /*
Config data persistence
*/}}
{{- define "config.persistence.data" -}}
{{- if .Values.persistence.data }}
- name: POLYAXON_PERSISTENCE_DATA
  value: {{ toJson .Values.persistence.data | quote }}
{{- else }}
- name: POLYAXON_PERSISTENCE_DATA
  value: {{ toJson .Values.defaultPersistence.data | quote }}
{{- end }}
{{- end -}}

{{- /*
Config outputs persistence
*/}}
{{- define "config.persistence.outputs" -}}
{{- if .Values.persistence.outputs }}
- name: POLYAXON_PERSISTENCE_OUTPUTS
  value: {{ toJson .Values.persistence.outputs | quote }}
- name: POLYAXON_PERSISTENCE_OUTPUTS
  value: {{ toJson .Values.defaultPersistence.outputs | quote }}
{{- end }}
{{- end -}}

{{- /*
Config logs persistence
*/}}
{{- define "config.persistence.logs" -}}
{{- if .Values.persistence.logs }}
- name: POLYAXON_PERSISTENCE_LOGS
  value: {{ toJson .Values.persistence.logs | quote }}
{{- end }}
{{- end -}}

{{- /*
Config repos persistence
*/}}
{{- define "config.persistence.repos" -}}
{{- if .Values.persistence.repos }}
- name: POLYAXON_PERSISTENCE_REPOS
  value: {{ toJson .Values.persistence.repos | quote }}
{{- end }}
{{- end -}}

{{- /*
Config upload persistence
*/}}
{{- define "config.persistence.upload" -}}
{{- if .Values.persistence.upload }}
- name: POLYAXON_PERSISTENCE_UPLOAD
  value: {{ toJson .Values.persistence.upload | quote }}
{{- end }}
{{- end -}}

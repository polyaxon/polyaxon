{{/*
registry config
*/}}
{{- define "config.registry" }}
- name: POLYAXON_REGISTRY_HOST
  value: {{ template "docker-registry.fullname" . }}
- name: POLYAXON_REGISTRY_PORT
  value: {{ (index .Values "docker-registry").service.port | quote }}
- name: POLYAXON_REGISTRY_NODE_PORT
  value: {{ (index .Values "docker-registry").service.nodePort | quote }}
{{- end }}

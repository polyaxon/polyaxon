{{/*
Config data persistence
*/}}
{{- define "config.persistence.data" }}
{{- if .Values.persistence.data }}
- name: POLYAXON_PERSISTENCE_DATA
  value: {{ toJson .Values.persistence.data | quote }}
{{- else if .Values.nfsProvisioner.enabled }}
- name: POLYAXON_PERSISTENCE_DATA
  value: {{ ( toJson ( dict "data" (dict "mountPath" .Values.nfsProvisioner.pvc.data.mountPath "existingClaim" .Values.nfsProvisioner.pvc.data.name))) | quote }}
{{- end }}
{{- end -}}

{{/*
Config outputs persistence
*/}}
{{- define "config.persistence.outputs" }}
{{- if .Values.persistence.outputs }}
- name: POLYAXON_PERSISTENCE_OUTPUTS
  value: {{ toJson .Values.persistence.outputs | quote }}
{{- else if .Values.nfsProvisioner.enabled }}
- name: POLYAXON_PERSISTENCE_OUTPUTS
  value: {{ ( toJson ( dict "outputs" (dict "mountPath" .Values.nfsProvisioner.pvc.outputs.mountPath "existingClaim" .Values.nfsProvisioner.pvc.outputs.name))) | quote }}
{{- end }}
{{- end -}}

{{/*
Config logs persistence
*/}}
{{- define "config.persistence.logs" }}
{{- if .Values.persistence.logs }}
- name: POLYAXON_PERSISTENCE_LOGS
  value: {{ toJson .Values.persistence.logs | quote }}
{{- else if .Values.nfsProvisioner.enabled }}
- name: POLYAXON_PERSISTENCE_LOGS
  value: {{ toJson (dict "mountPath" .Values.nfsProvisioner.pvc.logs.mountPath "existingClaim" .Values.nfsProvisioner.pvc.logs.name) | quote }}
{{- end }}
{{- end -}}

{{/*
Config repos persistence
*/}}
{{- define "config.persistence.repos" }}
{{- if .Values.persistence.repos }}
- name: POLYAXON_PERSISTENCE_REPOS
  value: {{ toJson .Values.persistence.repos | quote }}
{{- else if .Values.nfsProvisioner.enabled }}
- name: POLYAXON_PERSISTENCE_REPOS
  value: {{ toJson (dict "mountPath" .Values.nfsProvisioner.pvc.repos.mountPath "existingClaim" .Values.nfsProvisioner.pvc.repos.name) | quote }}
{{- end }}
{{- end -}}


{{/*
Config upload persistence
*/}}
{{- define "config.persistence.upload" }}
{{- if .Values.persistence.upload }}
- name: POLYAXON_PERSISTENCE_UPLOAD
  value: {{ toJson .Values.persistence.upload | quote }}
{{- else if .Values.nfsProvisioner.enabled }}
- name: POLYAXON_PERSISTENCE_UPLOAD
  value: {{ toJson .Values.nfsProvisioner.pvc.upload | quote }}
{{- end }}
{{- end -}}

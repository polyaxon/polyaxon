{{/*
Config claim_names
*/}}
{{- define "config.claim_names" }}
- name: POLYAXON_CLAIM_NAMES_DATA
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.data.existingClaim }}
  value: {{ .Values.persistence.data.existingClaim | default .Values.nfsProvisioner.pvc.data.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_OUTPUTS
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.outputs.existingClaim }}
  value: {{ .Values.persistence.outputs.existingClaim | default .Values.nfsProvisioner.pvc.outputs.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_LOGS
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.logs.existingClaim }}
  value: {{ .Values.persistence.logs.existingClaim | default .Values.nfsProvisioner.pvc.logs.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_UPLOAD
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.upload.existingClaim }}
  value: {{ .Values.persistence.upload.existingClaim | default .Values.nfsProvisioner.pvc.upload.name }}
{{- else }}
  value: ""
{{- end }}
- name: POLYAXON_CLAIM_NAMES_REPOS
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.repos.existingClaim }}
  value: {{ .Values.persistence.repos.existingClaim | default .Values.nfsProvisioner.pvc.repos.name }}
{{- else }}
  value: ""
{{- end }}
{{- end -}}

{{/*
Config mount_paths
*/}}
{{- define "config.mount_paths" }}
- name: POLYAXON_MOUNT_PATHS_UPLOAD
  value: {{ .Values.persistence.upload.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_DATA
  value: {{ .Values.persistence.data.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_LOGS
  value: {{ .Values.persistence.logs.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_OUTPUTS
  value: {{ .Values.persistence.outputs.mountPath | quote }}
- name: POLYAXON_MOUNT_PATHS_REPOS
  value: {{ .Values.persistence.repos.mountPath | quote }}
{{- end -}}

{{/*
Config sub_paths
*/}}
{{- define "config.sub_paths" }}
- name: POLYAXON_SUB_PATHS_UPLOAD
  value: {{ .Values.persistence.upload.subPath | quote }}
- name: POLYAXON_SUB_PATHS_DATA
  value: {{ .Values.persistence.data.subPath | quote }}
- name: POLYAXON_SUB_PATHS_LOGS
  value: {{ .Values.persistence.logs.subPath | quote }}
- name: POLYAXON_SUB_PATHS_OUTPUTS
  value: {{ .Values.persistence.outputs.subPath | quote }}
- name: POLYAXON_SUB_PATHS_REPOS
  value: {{ .Values.persistence.repos.subPath | quote }}
{{- end -}}

{{/*
Config extra_data
*/}}
{{- define "config.extra_data" }}
- name: POLYAXON_EXTRA_PERSISTENCES
  value: {{ toJson .Values.persistence.extra | quote }}
{{- end -}}

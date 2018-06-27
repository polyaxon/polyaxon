{{/*
Volume mounts
*/}}
{{- define "volumes.volumeMounts.upload" }}
- mountPath: {{ .Values.persistence.upload.mountPath }}
  name: upload
  {{ if .Values.persistence.upload.subPath -}}
  subPath: {{ .Values.persistence.upload.subPath | quote }}
  {{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.data" }}
- mountPath: {{ .Values.persistence.data.mountPath }}
  name: data
  {{ if .Values.persistence.data.subPath -}}
  subPath: {{ .Values.persistence.data.subPath | quote }}
  {{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.logs" }}
- mountPath: {{ .Values.persistence.logs.mountPath }}
  name: logs
  {{ if .Values.persistence.logs.subPath -}}
  subPath: {{ .Values.persistence.logs.subPath | quote }}
  {{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.outputs" }}
- mountPath: {{ .Values.persistence.outputs.mountPath }}
  name: outputs
  {{ if .Values.persistence.outputs.subPath -}}
  subPath: {{ .Values.persistence.outputs.subPath | quote }}
  {{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.repos" }}
- mountPath: {{ .Values.persistence.repos.mountPath }}
  name: repos
  {{ if .Values.persistence.repos.subPath -}}
  subPath: {{ .Values.persistence.repos.subPath | quote }}
  {{- end }}
{{- end -}}

{{/*
Volumes
*/}}
{{- define "volumes.volumes.upload" }}
- name: upload
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.upload.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.upload.existingClaim | default .Values.nfsProvisioner.pvc.upload.name }}
{{- else }}
  hostPath:
    path:  {{ .Values.persistence.upload.mountPath }}
{{ end }}
{{- end -}}
{{- define "volumes.volumes.repos" }}
- name: repos
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.repos.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.repos.existingClaim | default .Values.nfsProvisioner.pvc.repos.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.repos.mountPath }}
{{ end }}
{{- end -}}
{{- define "volumes.volumes.logs" }}
- name: logs
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.logs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.logs.existingClaim | default .Values.nfsProvisioner.pvc.logs.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.logs.mountPath }}
{{ end }}
{{- end -}}
{{- define "volumes.volumes.data" }}
- name: data
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.data.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.data.existingClaim | default .Values.nfsProvisioner.pvc.data.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.data.mountPath }}
{{ end }}
{{- end -}}
{{- define "volumes.volumes.outputs" }}
- name: outputs
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.outputs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.outputs.existingClaim | default .Values.nfsProvisioner.pvc.outputs.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.outputs.mountPath }}
{{ end }}
{{- end -}}


{{/*
Dirs
*/}}
{{- define "volumes.dirs" }}
- name: docker
  hostPath:
    path: {{ .Values.dirs.docker | quote }}
{{- if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: nvidia-lib
  hostPath:
    path: {{ .Values.dirs.nvidia.lib | quote }}
- name: nvidia-bin
  hostPath:
    path: {{ .Values.dirs.nvidia.bin | quote }}
- name: nvidia-libcuda
  hostPath:
    path: {{ .Values.dirs.nvidia.libcuda | quote }}
{{- end }}
{{- end -}}


{{/*
Dir mounts
*/}}
{{- define "volumes.dirMounts" }}
- name: docker
  mountPath: {{ .Values.mountPaths.docker }}
{{- if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: nvidia-lib
{{- if .Values.mountPaths.nvidia.lib }}
  mountPath: {{ .Values.mountPaths.nvidia.lib | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.lib | quote }}
{{- end }}
- name: nvidia-bin
{{- if .Values.mountPaths.nvidia.bin }}
  mountPath: {{ .Values.mountPaths.nvidia.bin | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.bin | quote }}
{{- end }}
- name: nvidia-libcuda
{{- if .Values.mountPaths.nvidia.libcuda }}
  mountPath: {{ .Values.mountPaths.nvidia.libcuda | quote }}
{{- else }}
  mountPath: {{ .Values.dirs.nvidia.libcuda | quote }}
{{- end }}
{{- end }}
{{- end -}}

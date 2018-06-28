{{/*
Volume mounts
*/}}
{{- define "volumes.volumeMounts.upload" }}
{{- if .Values.persistence.upload }}
- mountPath: {{ .Values.persistence.upload.mountPath }}
  name: upload
  {{ if .Values.persistence.upload.subPath -}}
  subPath: {{ .Values.persistence.upload.subPath | quote }}
  {{- end }}
{{- else if .Values.nfsProvisioner.enabled }}
- mountPath: {{ .Values.nfsProvisioner.pvc.upload.mountPath }}
  name: upload
{{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.logs" }}
{{- if .Values.persistence.logs }}
- mountPath: {{ .Values.persistence.logs.mountPath }}
  name: logs
  {{ if .Values.persistence.logs.subPath -}}
  subPath: {{ .Values.persistence.logs.subPath | quote }}
  {{- end }}
{{- else if .Values.nfsProvisioner.enabled }}
- mountPath: {{ .Values.nfsProvisioner.pvc.logs.mountPath }}
  name: logs
{{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.repos" }}
{{- if .Values.persistence.repos }}
- mountPath: {{ .Values.persistence.repos.mountPath }}
  name: repos
  {{ if .Values.persistence.repos.subPath -}}
  subPath: {{ .Values.persistence.repos.subPath | quote }}
  {{- end }}
{{- else if .Values.nfsProvisioner.enabled }}
- mountPath: {{ .Values.nfsProvisioner.pvc.repos.mountPath }}
  name: repos
{{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.data" }}
{{- if .Values.persistence.data }}
{{- range $key, $val := .Values.persistence.data }}
- mountPath: {{ $val.mountPath }}
  name: {{ $key }}
  {{ if $val.subPath -}}
  subPath: {{ $val.subPath | quote }}
  {{- end }}
{{- end}}
{{- else if .Values.nfsProvisioner.enabled }}
- mountPath: {{ .Values.nfsProvisioner.pvc.data.mountPath }}
  name: data
{{- end }}
{{- end -}}
{{- define "volumes.volumeMounts.outputs" }}
{{- if .Values.persistence.outputs }}
{{- range $key, $val := .Values.persistence.outputs }}
- mountPath: {{ $val.mountPath }}
  name: {{ $key }}
  {{ if $val.subPath -}}
  subPath: {{ $val.subPath | quote }}
  {{- end }}
{{- end}}
{{- else if .Values.nfsProvisioner.enabled }}
- mountPath: {{ .Values.nfsProvisioner.pvc.outputs.mountPath }}
  name: outputs
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
    path:  {{ .Values.persistence.upload.hostPath | .Values.persistence.upload.mountPath }}
{{- end }}
{{- end -}}
{{- define "volumes.volumes.repos" }}
- name: repos
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.repos.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.repos.existingClaim | default .Values.nfsProvisioner.pvc.repos.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.repos.hostPath | .Values.persistence.repos.mountPath }}
{{- end }}
{{- end -}}
{{- define "volumes.volumes.logs" }}
- name: logs
{{- if or .Values.nfsProvisioner.enabled .Values.persistence.logs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.logs.existingClaim | default .Values.nfsProvisioner.pvc.logs.name }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.logs.hostPath | .Values.persistence.logs.mountPath }}
{{- end }}
{{- end -}}
{{- define "volumes.volumes.data" }}
{{- if .Values.persistence.data }}
{{- range $key, $val := .Values.persistence.data }}
- name: {{ $key }}
{{- if $val.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ $val.existingClaim }}
{{- else }}
  hostPath:
    path: {{ $val.hostPath | $val.mountPath }}
{{- end }}
{{- end}}
{{- else if .Values.nfsProvisioner.enabled }}
- name: data
  persistentVolumeClaim:
    claimName: {{ .Values.nfsProvisioner.pvc.data.name }}
{{- end }}
{{- end -}}
{{- define "volumes.volumes.outputs" }}
{{- if .Values.persistence.outputs }}
{{- range $key, $val := .Values.persistence.outputs }}
- name: {{ $key }}
{{- if $val.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ $val.existingClaim }}
{{- else }}
  hostPath:
    path: {{ $val.hostPath | $val.mountPath }}
{{- end }}
{{- end}}
{{- else if .Values.nfsProvisioner.enabled }}
- name: outputs
  persistentVolumeClaim:
    claimName: {{ .Values.nfsProvisioner.pvc.outputs.name }}
{{- end }}
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

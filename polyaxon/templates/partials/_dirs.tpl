{{/*
Config dirs
*/}}
{{- define "config.dirs" }}
- name: POLYAXON_DIRS_DOCKER
  value: {{ .Values.dirs.docker | quote }}
- name: POLYAXON_DIRS_NVIDIA
  value: {{ toJson .Values.dirs.nvidia | quote }}
{{- if .Values.mountPaths.docker }}
- name: POLYAXON_MOUNT_PATHS_DOCKER
  value: {{ toJson .Values.mountPaths.docker | quote }}
{{- else }}
- name: POLYAXON_MOUNT_PATHS_DOCKER
  value: {{ toJson .Values.dirs.docker | quote }}
{{- end }}
{{- if and .Values.mountPaths.nvidia.lib .Values.mountPaths.nvidia.bin .Values.mountPaths.nvidia.libcuda }}
- name: POLYAXON_MOUNT_PATHS_NVIDIA
  value: {{ toJson .Values.mountPaths.nvidia | quote }}
- name: LD_LIBRARY_PATH
  value: "{{ .Values.mountPaths.nvidia.lib }}:{{ .Values.mountPaths.nvidia.libcuda }}"
{{- else if and .Values.dirs.nvidia.lib .Values.dirs.nvidia.bin .Values.dirs.nvidia.libcuda }}
- name: POLYAXON_MOUNT_PATHS_NVIDIA
  value: {{ toJson .Values.dirs.nvidia | quote }}
- name: LD_LIBRARY_PATH
  value: "{{ .Values.dirs.nvidia.lib }}:{{ .Values.dirs.nvidia.libcuda }}"
{{- end }}
{{- end -}}

{{- /*
Volume mounts
*/}}
{{- define "volumes.volumeMounts.upload" -}}
{{- if .Values.persistence.upload }}
- mountPath: {{ .Values.persistence.upload.mountPath | quote }}
  name: upload
  {{ if .Values.persistence.upload.subPath -}}
  subPath: {{ .Values.persistence.upload.subPath | quote }}
  {{- end }}
{{- end }}
{{- end -}}  {{- /* end def upload volume mounts */ -}}
{{- define "volumes.volumeMounts.logs" -}}
{{- if .Values.persistence.logs }}
{{- if not .Values.persistence.logs.store }}
- mountPath: {{ .Values.persistence.logs.mountPath | quote }}
  name: logs
  {{ if .Values.persistence.logs.subPath -}}
  subPath: {{ .Values.persistence.logs.subPath | quote }}
  {{- end }}
{{- end }}  {{- /* end if store */ -}}
{{- end }}
{{- end -}}  {{- /* end def logs volume mounts */ -}}
{{- define "volumes.volumeMounts.repos" -}}
{{- if .Values.persistence.repos }}
- mountPath: {{ .Values.persistence.repos.mountPath | quote }}
  name: repos
  {{ if .Values.persistence.repos.subPath -}}
  subPath: {{ .Values.persistence.repos.subPath | quote }}
  {{- end }}
{{- end }}
{{- end -}}  {{- /* end def repos volume mounts */ -}}
{{- define "volumes.volumeMounts.data" -}}
{{- if .Values.persistence.data }}
{{- range $key, $val := .Values.persistence.data }}
{{- if not $val.store }}
- mountPath: {{ $val.mountPath | quote }}
  name: {{ $key }}
  {{ if $val.subPath -}}
  subPath: {{ $val.subPath | quote }}
  {{- end }}
{{- end }}  {{- /* end if store */ -}}
{{- end }}  {{- /* end range */ -}}
{{- else }}
- mountPath: {{ .Values.defaultPersistence.data.data.mountPath | quote }}
  name: data
{{- end }}
{{- end -}}  {{- /* end def data volume mounts */ -}}
{{- define "volumes.volumeMounts.outputs" -}}
{{- if .Values.persistence.outputs }}
{{- range $key, $val := .Values.persistence.outputs }}
{{- if not $val.store }}
- mountPath: {{ $val.mountPath | quote }}
  name: {{ $key }}
  {{ if $val.subPath -}}
  subPath: {{ $val.subPath | quote }}
  {{- end }}
{{- end }}  {{- /* end if store */ -}}
{{- end }}  {{- /* end range */ -}}
{{- else }}
- mountPath: {{ .Values.defaultPersistence.outputs.outputs.mountPath | quote }}
  name: outputs
{{- end }}
{{- end -}}  {{- /* end def outputs volume mounts */ -}}
{{- define "volumes.volumeMounts.ssl" -}}
{{- if and .Values.ssl.enabled .values.ssl.secretName }}
- name: polyaxon-ssl-volume
  secret:
    secretName: {{ .values.ssl.secretName | quote }}
{{- end }}
{{- end -}}  {{- /* end def upload volume mounts */ -}}

{{- /*
Volumes
*/}}
{{- define "volumes.volumes.upload" -}}
- name: upload
{{- if .Values.persistence.upload }}
{{- if .Values.persistence.upload.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.upload.existingClaim | quote }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.upload.hostPath | default .Values.persistence.upload.mountPath | quote }}
{{- end }}  {{- /* end persistence upload */ -}}
{{- end }}
{{- end -}}  {{- /* end def upload volume mounts */ -}}
{{- define "volumes.volumes.repos" -}}
- name: repos
{{- if .Values.persistence.repos }}
{{- if .Values.persistence.repos.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.repos.existingClaim | quote }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.repos.hostPath | default .Values.persistence.repos.mountPath | quote }}
{{- end }}  {{- /* end persistence repos */ -}}
{{- end }}
{{- end -}}  {{- /* end def repos volume mounts */ -}}
{{- define "volumes.volumes.logs" -}}
{{- if .Values.persistence.logs }}
{{- if not .Values.persistence.logs.store }}
- name: logs
{{- if .Values.persistence.logs.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ .Values.persistence.logs.existingClaim | quote }}
{{- else }}
  hostPath:
    path: {{ .Values.persistence.logs.hostPath | default .Values.persistence.logs.mountPath | quote }}
{{- end }}  {{- /* end persistence logs */ -}}
{{- end }} {{- /* end store check */ -}}
{{- end }}
{{- end -}}  {{- /* end def logs volume mounts */ -}}
{{- define "volumes.volumes.data" -}}
{{- if .Values.persistence.data }}
{{- range $key, $val := .Values.persistence.data }}
{{- if not $val.store }}
- name: {{ $key }}
{{- if $val.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ $val.existingClaim }}
{{- else }}
  hostPath:
    path: {{ $val.hostPath | default $val.mountPath | quote }}
{{- end }}
{{- end }} {{- /* end volume check */ -}}
{{- end}}  {{- /* end range */ -}}
{{- else }}
- name: data
  hostPath:
    path: {{ .Values.defaultPersistence.data.data.hostPath | quote }}
{{- end }}
{{- end -}}  {{- /* end def data volume mounts */ -}}
{{- define "volumes.volumes.outputs" -}}
{{- if .Values.persistence.outputs }}
{{- range $key, $val := .Values.persistence.outputs }}
{{- if not $val.store }}
- name: {{ $key }}
{{- if $val.existingClaim }}
  persistentVolumeClaim:
    claimName: {{ $val.existingClaim }}
{{- else }}
  hostPath:
    path: {{ $val.hostPath | default $val.mountPath | quote }}
{{- end }}
{{- end }} {{- /* end store check */ -}}
{{- end}}  {{- /* end range */ -}}
{{- else }}
- name: outputs
  hostPath:
    path: {{ .Values.defaultPersistence.outputs.outputs.hostPath | quote }}
{{- end }}
{{- end -}}  {{- /* end def outputs volume mounts */ -}}
{{- define "volumes.volumes.ssl" -}}
{{- if and .Values.ssl.enabled .values.ssl.secretName }}
- name: polyaxon-ssl-volume
  readOnly: true
  mountPath: {{ default "/etc/ssl" .Values.ssl.path | quote }}
{{- end }}
{{- end -}}  {{- /* end def upload volume mounts */ -}}

{{- /*
Dirs
*/}}
{{- define "volumes.dirs" -}}
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


{{- /*
Dir mounts
*/}}
{{- define "volumes.dirMounts" -}}
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

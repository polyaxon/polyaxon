{{- /*
apiHooks
*/}}
{{- define "config.apiHooks.image" -}}
{{- default .Values.api.image .Values.apiHooks.image -}}
{{- end -}}

{{- define "config.apiHooks.imageTag" -}}
{{- default .Values.api.imageTag .Values.apiHooks.imageTag -}}
{{- end -}}

{{- define "config.apiHooks.imagePullPolicy" -}}
{{- default .Values.api.imagePullPolicy .Values.apiHooks.imagePullPolicy -}}
{{- end -}}

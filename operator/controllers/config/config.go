package config

import "os"

const (
	// TFfJobEnabled is a flag to enable TFfJob conroller
	TFfJobEnabled = "POLYAXON_TFJOB_ENABLED"

	// PytorchJobEnabled is a flag to enable PytorchJob conroller
	PytorchJobEnabled = "POLYAXON_PYTORCH_JOB_ENABLED"

	// MpiJobEnabled is a flag to enable MpiJob conroller
	MpiJobEnabled = "POLYAXON_MPIJOB_ENABLED"
)

// GetStrEnv returns an environment str variable given by key or return a default value.
func GetStrEnv(key, defaultValue string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return defaultValue
}

// GetBoolEnv returns an environment bool variable given by key or return a default value.
func GetBoolEnv(key string, defaultValue bool) bool {
	if GetStrEnv(key, "false") == "true" {
		return true
	}
	return defaultValue
}

// KFEnabled return a flag to tell if Kubeflow is enabled
func KFEnabled() bool {
	return GetBoolEnv(TFfJobEnabled, false) || GetBoolEnv(PytorchJobEnabled, false) || GetBoolEnv(MpiJobEnabled, false)
}

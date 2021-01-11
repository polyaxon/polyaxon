/*
Copyright 2018-2021 Polyaxon, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package sparkapi

import (
	corev1 "k8s.io/api/core/v1"

	operationv1 "github.com/polyaxon/polyaxon/operator/api/v1"
)

// RestartPolicy is the policy of if and in which conditions the controller should restart a terminated application.
// This completely defines actions to be taken on any kind of Failures during an application run.
type RestartPolicy struct {
	// Type specifies the RestartPolicyType.
	// +kubebuilder:validation:Enum={Never,Always,OnFailure}
	Type corev1.RestartPolicy `json:"type,omitempty"`

	// OnSubmissionFailureRetries is the number of times to retry submitting an application before giving up.
	// This is best effort and actual retry attempts can be >= the value specified due to caching.
	// These are required if RestartPolicy is OnFailure.
	// +kubebuilder:validation:Minimum=0
	// +optional
	OnSubmissionFailureRetries *int32 `json:"onSubmissionFailureRetries,omitempty"`

	// OnFailureRetries the number of times to retry running an application before giving up.
	// +kubebuilder:validation:Minimum=0
	// +optional
	OnFailureRetries *int32 `json:"onFailureRetries,omitempty"`

	// OnSubmissionFailureRetryInterval is the interval between retries on failed submissions.
	// Interval to wait between successive retries of a failed application.
	// +kubebuilder:validation:Minimum=1
	// +optional
	OnSubmissionFailureRetryInterval *int64 `json:"onSubmissionFailureRetryInterval,omitempty"`

	// OnFailureRetryInterval is the interval between retries on failed runs.
	// +kubebuilder:validation:Minimum=1
	// +optional
	OnFailureRetryInterval *int64 `json:"onFailureRetryInterval,omitempty"`
}

// SparkApplicationSpec describes the specification of a Spark application using Kubernetes as a cluster manager.
// It carries every pieces of information a spark-submit command takes and recognizes.
type SparkApplicationSpec struct {
	// Type tells the type of the Spark application.
	Type operationv1.SparkApplicationType `json:"type"`
	// SparkVersion is the version of Spark the application uses.
	SparkVersion string `json:"sparkVersion"`
	// Mode is the deployment mode of the Spark application.
	Mode operationv1.SparkDeployMode `json:"mode,omitempty"`

	// ImagePullSecrets is the list of image-pull secrets.
	ImagePullSecrets []string `json:"imagePullSecrets,omitempty"`

	// MainClass is the fully-qualified main class of the Spark application.
	// This only applies to Java/Scala Spark applications.
	// +optional
	MainClass *string `json:"mainClass,omitempty"`

	// MainFile is the path to a bundled JAR, Python, or R file of the application.
	// +optional
	MainApplicationFile *string `json:"mainApplicationFile"`

	// Arguments is a list of arguments to be passed to the application.
	// +optional
	Arguments []string `json:"arguments,omitempty"`

	// SparkConf carries user-specified Spark configuration properties as they would use the  "--conf" option in
	// spark-submit.
	// +optional
	SparkConf map[string]string `json:"sparkConf,omitempty"`

	// HadoopConf carries user-specified Hadoop configuration properties as they would use the  the "--conf" option
	// in spark-submit.  The SparkApplication controller automatically adds prefix "spark.hadoop." to Hadoop
	// configuration properties.
	// +optional
	HadoopConf map[string]string `json:"hadoopConf,omitempty"`

	// SparkConfigMap carries the name of the ConfigMap containing Spark configuration files such as log4j.properties.
	// The controller will add environment variable SPARK_CONF_DIR to the path where the ConfigMap is mounted to.
	// +optional
	SparkConfigMap *string `json:"sparkConfigMap,omitempty"`

	// HadoopConfigMap carries the name of the ConfigMap containing Hadoop configuration files such as core-site.xml.
	// The controller will add environment variable HADOOP_CONF_DIR to the path where the ConfigMap is mounted to.
	// +optional
	HadoopConfigMap *string `json:"hadoopConfigMap,omitempty"`

	// Volumes is the list of Kubernetes volumes that can be mounted by the driver and/or executors.
	// +optional
	Volumes []corev1.Volume `json:"volumes,omitempty"`

	// Driver is the driver specification.
	Driver DriverSpec `json:"driver"`

	// Executor is the executor specification.
	Executor ExecutorSpec `json:"executor"`

	// RestartPolicy defines the policy on if and in which conditions the controller should restart an application.
	RestartPolicy RestartPolicy `json:"restartPolicy,omitempty"`

	// FailureRetries is the number of times to retry a failed application before giving up.
	// This is best effort and actual retry attempts can be >= the value specified.
	FailureRetries *int32 `json:"failureRetries,omitempty"`

	// RetryInterval is the unit of intervals in seconds between submission retries.
	RetryInterval *int64 `json:"retryInterval,omitempty"`

	// This sets the major Python version of the docker
	// image used to run the driver and executor containers. Can either be 2 or 3, default 2.
	PythonVersion *string `json:"pythonVersion,omitempty"`

	// This sets the Memory Overhead Factor that will allocate memory to non-JVM memory.
	// For JVM-based jobs this value will default to 0.10, for non-JVM jobs 0.40. Value of this field will
	// be overridden by `Spec.Driver.MemoryOverhead` and `Spec.Executor.MemoryOverhead` if they are set.
	MemoryOverheadFactor *string `json:"memoryOverheadFactor,omitempty"`

	// BatchScheduler configures which batch scheduler will be used for scheduling
	BatchScheduler *string `json:"batchScheduler,omitempty"`

	// TimeToLiveSeconds defines the Time-To-Live (TTL) duration in seconds for this SparkAplication
	// after its termination.
	// The SparkApplication object will be garbage collected if the current time is more than the
	// TimeToLiveSeconds since its termination.
	TimeToLiveSeconds *int64 `json:"timeToLiveSeconds,omitempty"`
}

// SparkPodSpec defines common things that can be customized for a Spark driver or executor pod.
type SparkPodSpec struct {
	// Cores maps to `spark.driver.cores` or `spark.executor.cores` for the driver and executors, respectively.
	Cores *int32 `json:"cores,omitempty"`

	// CoreLimit specifies a hard limit on CPU cores for the pod.
	CoreLimit *string `json:"coreLimit,omitempty"`

	// Memory is the amount of memory to request for the pod.
	Memory *string `json:"memory,omitempty"`

	// MemoryOverhead is the amount of off-heap memory to allocate in cluster mode, in MiB unless otherwise specified.
	MemoryOverhead *string `json:"memoryOverhead,omitempty"`

	// GPU specifies GPU requirement for the pod.
	GPU *GPUSpec `json:"gpu,omitempty"`

	// Image is the container image to use. Overrides Spec.Image if set.
	Image *string `json:"image,omitempty"`

	// Env carries the environment variables to add to the pod.	// +optional
	Env []corev1.EnvVar `json:"env,omitempty"`

	// EnvFrom is a list of sources to populate environment variables in the container.
	EnvFrom []corev1.EnvFromSource `json:"envFrom,omitempty"`

	// Labels are the Kubernetes labels to be added to the pod.
	Labels map[string]string `json:"labels,omitempty"`

	// Annotations are the Kubernetes annotations to be added to the pod.
	Annotations map[string]string `json:"annotations,omitempty"`

	// VolumeMounts specifies the volumes listed in ".spec.volumes" to mount into the main container's filesystem.
	VolumeMounts []corev1.VolumeMount `json:"volumeMounts,omitempty"`

	// Affinity specifies the affinity/anti-affinity settings for the pod.
	Affinity *corev1.Affinity `json:"affinity,omitempty"`

	// Tolerations specifies the tolerations listed in ".spec.tolerations" to be applied to the pod.
	Tolerations []corev1.Toleration `json:"tolerations,omitempty"`

	// SecurityContenxt specifies the PodSecurityContext to apply.
	SecurityContenxt *corev1.PodSecurityContext `json:"securityContext,omitempty"`

	// SchedulerName specifies the scheduler that will be used for scheduling
	SchedulerName *string `json:"schedulerName,omitempty"`

	// Sidecars is a list of sidecar containers that run along side the main Spark container.
	Sidecars []corev1.Container `json:"sidecars,omitempty"`

	// InitContainers is a list of init-containers that run to completion before the main Spark container.
	InitContainers []corev1.Container `json:"initContainers,omitempty"`

	// HostNetwork indicates whether to request host networking for the pod or not.
	HostNetwork *bool `json:"hostNetwork,omitempty"`

	// NodeSelector is the Kubernetes node selector to be added to the driver and executor pods.
	NodeSelector map[string]string `json:"nodeSelector,omitempty"`

	// DnsConfig dns settings for the pod, following the Kubernetes specifications.
	DNSConfig *corev1.PodDNSConfig `json:"dnsConfig,omitempty"`
}

// DriverSpec is specification of the driver.
type DriverSpec struct {
	SparkPodSpec `json:",inline"`
	// PodName is the name of the driver pod that the user creates. This is used for the
	// in-cluster client mode in which the user creates a client pod where the driver of
	// the user application runs. It's an error to set this field if Mode is not
	// in-cluster-client.
	// +optional
	// +kubebuilder:validation:Pattern=[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*
	PodName *string `json:"podName,omitempty"`
	// CoreRequest is the physical CPU core request for the driver.
	// Maps to `spark.kubernetes.driver.request.cores` that is available since Spark 3.0.
	// +optional
	CoreRequest *string `json:"coreRequest,omitempty"`
	// ServiceAccount is the name of the Kubernetes service account used by the driver pod
	// when requesting executor pods from the API server.
	// +optional
	ServiceAccount *string `json:"serviceAccount,omitempty"`
	// JavaOptions is a string of extra JVM options to pass to the driver. For instance,
	// GC settings or other logging.
	// +optional
	JavaOptions *string `json:"javaOptions,omitempty"`
}

// ExecutorSpec is specification of the executor.
type ExecutorSpec struct {
	SparkPodSpec `json:",inline"`
	// Instances is the number of executor instances.
	// +optional
	// +kubebuilder:validation:Minimum=1
	Instances *int32 `json:"instances,omitempty"`
	// CoreRequest is the physical CPU core request for the executors.
	// Maps to `spark.kubernetes.executor.request.cores` that is available since Spark 2.4.
	// +optional
	CoreRequest *string `json:"coreRequest,omitempty"`
	// JavaOptions is a string of extra JVM options to pass to the executors. For instance,
	// GC settings or other logging.
	// +optional
	JavaOptions *string `json:"javaOptions,omitempty"`
	// DeleteOnTermination specify whether executor pods should be deleted in case of failure or normal termination.
	// Maps to `spark.kubernetes.executor.deleteOnTermination` that is available since Spark 3.0.
	// +optional
	DeleteOnTermination *bool `json:"deleteOnTermination,omitempty"`
}

type GPUSpec struct {
	// Name is GPU resource name, such as: nvidia.com/gpu or amd.com/gpu
	Name string `json:"name"`
	// Quantity is the number of GPUs to request for driver or executor.
	Quantity int64 `json:"quantity"`
}

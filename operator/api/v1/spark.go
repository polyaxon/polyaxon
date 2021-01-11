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

package v1

import (
	corev1 "k8s.io/api/core/v1"
)

// SparkJobSpec defines the desired state of a spark job
// +k8s:openapi-gen=true
type SparkJobSpec struct {
	// Type tells the type of the Spark application.
	// +kubebuilder:validation:Enum={Java,Python,Scala,R}
	Type SparkApplicationType `json:"type" protobuf:"bytes,1,opt,name=type"`

	// SparkVersion is the version of Spark the application uses.
	SparkVersion string `json:"sparkVersion" protobuf:"bytes,2,opt,name=sparkVersion"`

	// Mode is the deployment mode of the Spark application.
	// +kubebuilder:validation:Enum={cluster,client}
	Mode SparkDeployMode `json:"mode,omitempty" protobuf:"bytes,3,opt,name=mode"`

	// MainClass is the fully-qualified main class of the Spark application.
	// This only applies to Java/Scala Spark applications.
	// +optional
	MainClass *string `json:"mainClass,omitempty" protobuf:"bytes,4,opt,name=mainClass"`

	// MainFile is the path to a bundled JAR, Python, or R file of the application.
	// +optional
	MainApplicationFile *string `json:"mainApplicationFile" protobuf:"bytes,5,opt,name=mainApplicationFile"`

	// Arguments is a list of arguments to be passed to the application.
	// +optional
	Arguments []string `json:"arguments,omitempty" protobuf:"bytes,6,opt,name=arguments"`

	// SparkConf carries user-specified Spark configuration properties as they would use the  "--conf" option in
	// spark-submit.
	// +optional
	SparkConf map[string]string `json:"sparkConf,omitempty" protobuf:"bytes,7,opt,name=sparkConf"`

	// HadoopConf carries user-specified Hadoop configuration properties as they would use the  the "--conf" option
	// in spark-submit.  The SparkApplication controller automatically adds prefix "spark.hadoop." to Hadoop
	// configuration properties.
	// +optional
	HadoopConf map[string]string `json:"hadoopConf,omitempty" protobuf:"bytes,8,opt,name=hadoopConf"`

	// SparkConfigMap carries the name of the ConfigMap containing Spark configuration files such as log4j.properties.
	// The controller will add environment variable SPARK_CONF_DIR to the path where the ConfigMap is mounted to.
	// +optional
	SparkConfigMap *string `json:"sparkConfigMap,omitempty" protobuf:"bytes,9,opt,name=sparkConfigMap"`

	// HadoopConfigMap carries the name of the ConfigMap containing Hadoop configuration files such as core-site.xml.
	// The controller will add environment variable HADOOP_CONF_DIR to the path where the ConfigMap is mounted to.
	// +optional
	HadoopConfigMap *string `json:"hadoopConfigMap,omitempty" protobuf:"bytes,10,opt,name=hadoopConfigMap"`

	// Volumes is the list of Kubernetes volumes that can be mounted by the driver and/or executors.
	// +optional
	Volumes []corev1.Volume `json:"volumes,omitempty" protobuf:"bytes,11,opt,name=volumes"`

	// Spark executor definition
	Executor SparkReplicaSpec `json:"executor" protobuf:"bytes,12,opt,name=executor"`

	// Spark driver definition
	Driver SparkReplicaSpec `json:"driver" protobuf:"bytes,13,opt,name=driver"`
}

// SparkReplicaSpec is a description of a spark replica
// +k8s:openapi-gen=true
type SparkReplicaSpec struct {
	// Replicas is the desired number of replicas of the given template.
	// If unspecified, defaults to 1.
	Replicas *int32 `json:"replicas,omitempty"`

	// Template is the object that describes the pod that
	// will be created for this replica. RestartPolicy in PodTemplateSpec
	// will be overide by RestartPolicy in ReplicaSpec
	Template corev1.PodTemplateSpec `json:"template,omitempty"`
}

// SparkApplicationType describes the type of a Spark application.
type SparkApplicationType string

// Different types of Spark applications.
const (
	SparkJavaApplicationType   SparkApplicationType = "Java"
	SparkScalaApplicationType  SparkApplicationType = "Scala"
	SparkPythonApplicationType SparkApplicationType = "Python"
	SparkRApplicationType      SparkApplicationType = "R"
)

// SparkDeployMode describes the type of deployment of a Spark application.
type SparkDeployMode string

// Different types of deployments.
const (
	SparkClusterMode         SparkDeployMode = "cluster"
	SparkClientMode          SparkDeployMode = "client"
	SparkInClusterClientMode SparkDeployMode = "in-cluster-client"
)

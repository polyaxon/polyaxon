# PolyaxonSdk.V1Spark

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to 'spark']
**connections** | **[String]** |  | [optional] 
**volumes** | [**[V1Volume]**](V1Volume.md) | Volumes is a list of volumes that can be mounted. | [optional] 
**type** | [**V1SparkType**](V1SparkType.md) | Type tells the type of the Spark application. | [optional] 
**spark_version** | **String** | Spark version is the version of Spark the application uses. | [optional] 
**python_version** | **String** | Spark version is the version of Spark the application uses. | [optional] 
**deploy_mode** | [**SparkDeployMode**](SparkDeployMode.md) | Mode is the deployment mode of the Spark application. | [optional] 
**main_class** | **String** | MainClass is the fully-qualified main class of the Spark application. This only applies to Java/Scala Spark applications. | [optional] 
**main_application_file** | **String** | MainFile is the path to a bundled JAR, Python, or R file of the application. | [optional] 
**_arguments** | **[String]** | Arguments is a list of arguments to be passed to the application. | [optional] 
**hadoop_conf** | **{String: String}** | HadoopConf carries user-specified Hadoop configuration properties as they would use the  the \"--conf\" option in spark-submit.  The SparkApplication controller automatically adds prefix \"spark.hadoop.\" to Hadoop configuration properties. | [optional] 
**spark_conf** | **{String: String}** | HadoopConf carries user-specified Hadoop configuration properties as they would use the  the \"--conf\" option in spark-submit.  The SparkApplication controller automatically adds prefix \"spark.hadoop.\" to Hadoop configuration properties. | [optional] 
**spark_config_map** | **String** | SparkConfigMap carries the name of the ConfigMap containing Spark configuration files such as log4j.properties. The controller will add environment variable SPARK_CONF_DIR to the path where the ConfigMap is mounted to. | [optional] 
**hadoop_config_map** | **String** | HadoopConfigMap carries the name of the ConfigMap containing Hadoop configuration files such as core-site.xml. The controller will add environment variable HADOOP_CONF_DIR to the path where the ConfigMap is mounted to. | [optional] 
**executor** | [**V1SparkReplica**](V1SparkReplica.md) |  | [optional] 
**driver** | [**V1SparkReplica**](V1SparkReplica.md) |  | [optional] 



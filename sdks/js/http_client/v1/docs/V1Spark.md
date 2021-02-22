# PolyaxonSdk.V1Spark

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to &#39;spark&#39;]
**connections** | **[String]** |  | [optional] 
**volumes** | **[Object]** | Volumes is a list of volumes that can be mounted. | [optional] 
**type** | [**V1SparkType**](V1SparkType.md) |  | [optional] 
**sparkVersion** | **String** | Spark version is the version of Spark the application uses. | [optional] 
**pythonVersion** | **String** | Spark version is the version of Spark the application uses. | [optional] 
**deployMode** | [**SparkDeployMode**](SparkDeployMode.md) |  | [optional] 
**mainClass** | **String** | MainClass is the fully-qualified main class of the Spark application. This only applies to Java/Scala Spark applications. | [optional] 
**mainApplicationFile** | **String** | MainFile is the path to a bundled JAR, Python, or R file of the application. | [optional] 
**_arguments** | **[String]** | Arguments is a list of arguments to be passed to the application. | [optional] 
**hadoopConf** | **{String: String}** | HadoopConf carries user-specified Hadoop configuration properties as they would use the  the \&quot;--conf\&quot; option in spark-submit.  The SparkApplication controller automatically adds prefix \&quot;spark.hadoop.\&quot; to Hadoop configuration properties. | [optional] 
**sparkConf** | **{String: String}** | HadoopConf carries user-specified Hadoop configuration properties as they would use the  the \&quot;--conf\&quot; option in spark-submit.  The SparkApplication controller automatically adds prefix \&quot;spark.hadoop.\&quot; to Hadoop configuration properties. | [optional] 
**sparkConfigMap** | **String** | SparkConfigMap carries the name of the ConfigMap containing Spark configuration files such as log4j.properties. The controller will add environment variable SPARK_CONF_DIR to the path where the ConfigMap is mounted to. | [optional] 
**hadoopConfigMap** | **String** | HadoopConfigMap carries the name of the ConfigMap containing Hadoop configuration files such as core-site.xml. The controller will add environment variable HADOOP_CONF_DIR to the path where the ConfigMap is mounted to. | [optional] 
**executor** | [**V1SparkReplica**](V1SparkReplica.md) |  | [optional] 
**driver** | [**V1SparkReplica**](V1SparkReplica.md) |  | [optional] 



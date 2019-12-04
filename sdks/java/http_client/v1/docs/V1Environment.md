
# V1Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resources** | [**V1ResourceRequirements**](V1ResourceRequirements.md) |  |  [optional]
**labels** | **Map&lt;String, String&gt;** |  |  [optional]
**annotations** | **Map&lt;String, String&gt;** |  |  [optional]
**nodeSelector** | **Map&lt;String, String&gt;** |  |  [optional]
**affinity** | **List&lt;Object&gt;** |  |  [optional]
**tolerations** | **List&lt;Object&gt;** |  |  [optional]
**serviceAccount** | **String** |  |  [optional]
**imagePullSecrets** | **List&lt;String&gt;** |  |  [optional]
**envVars** | **List&lt;Object&gt;** |  |  [optional]
**securityContext** | **Object** |  |  [optional]
**logLevel** | **String** |  |  [optional]
**auth** | **Boolean** |  |  [optional]
**docker** | **Boolean** |  |  [optional]
**shm** | **Boolean** |  |  [optional]
**outputs** | **Boolean** |  |  [optional]
**logs** | **Boolean** |  |  [optional]
**registry** | **String** |  |  [optional]
**initContainer** | [**V1ContainerEnv**](V1ContainerEnv.md) |  |  [optional]
**sidecarContainer** | [**V1ContainerEnv**](V1ContainerEnv.md) |  |  [optional]




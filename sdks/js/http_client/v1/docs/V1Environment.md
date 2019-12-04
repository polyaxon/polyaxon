# PolyaxonSdk.V1Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resources** | [**V1ResourceRequirements**](V1ResourceRequirements.md) |  | [optional] 
**labels** | **{String: String}** |  | [optional] 
**annotations** | **{String: String}** |  | [optional] 
**node_selector** | **{String: String}** |  | [optional] 
**affinity** | **[Object]** |  | [optional] 
**tolerations** | **[Object]** |  | [optional] 
**service_account** | **String** |  | [optional] 
**image_pull_secrets** | **[String]** |  | [optional] 
**env_vars** | **[Object]** |  | [optional] 
**security_context** | **Object** |  | [optional] 
**log_level** | **String** |  | [optional] 
**auth** | **Boolean** |  | [optional] 
**docker** | **Boolean** |  | [optional] 
**shm** | **Boolean** |  | [optional] 
**outputs** | **Boolean** |  | [optional] 
**logs** | **Boolean** |  | [optional] 
**registry** | **String** |  | [optional] 
**init_container** | [**V1ContainerEnv**](V1ContainerEnv.md) |  | [optional] 
**sidecar_container** | [**V1ContainerEnv**](V1ContainerEnv.md) |  | [optional] 



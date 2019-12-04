# V1Environment

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resources** | [**V1ResourceRequirements**](V1ResourceRequirements.md) |  | [optional] 
**labels** | **dict(str, str)** |  | [optional] 
**annotations** | **dict(str, str)** |  | [optional] 
**node_selector** | **dict(str, str)** |  | [optional] 
**affinity** | **list[object]** |  | [optional] 
**tolerations** | **list[object]** |  | [optional] 
**service_account** | **str** |  | [optional] 
**image_pull_secrets** | **list[str]** |  | [optional] 
**env_vars** | **list[object]** |  | [optional] 
**security_context** | **object** |  | [optional] 
**log_level** | **str** |  | [optional] 
**auth** | **bool** |  | [optional] 
**docker** | **bool** |  | [optional] 
**shm** | **bool** |  | [optional] 
**outputs** | **bool** |  | [optional] 
**logs** | **bool** |  | [optional] 
**registry** | **str** |  | [optional] 
**init_container** | [**V1ContainerEnv**](V1ContainerEnv.md) |  | [optional] 
**sidecar_container** | [**V1ContainerEnv**](V1ContainerEnv.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



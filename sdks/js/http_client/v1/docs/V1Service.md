# PolyaxonSdk.V1Service

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to 'service']
**environment** | [**V1Environment**](V1Environment.md) |  | [optional] 
**connections** | **[String]** |  | [optional] 
**volumes** | [**[V1Volume]**](V1Volume.md) | Volumes is a list of volumes that can be mounted. | [optional] 
**init** | [**[V1Init]**](V1Init.md) |  | [optional] 
**sidecars** | [**[V1Container]**](V1Container.md) |  | [optional] 
**container** | [**V1Container**](V1Container.md) |  | [optional] 
**ports** | **[Number]** |  | [optional] 
**rewritePath** | **Boolean** | Rewrite path to remove polyaxon base url(i.e. /v1/services/namespace/owner/project/). Default is false, the service shoud handle a base url. | [optional] 



# PolyaxonSdk.V1Service

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to &#39;service&#39;]
**environment** | [**V1Environment**](V1Environment.md) |  | [optional] 
**connections** | **[String]** |  | [optional] 
**volumes** | **[Object]** | Volumes is a list of volumes that can be mounted. | [optional] 
**init** | [**[V1Init]**](V1Init.md) |  | [optional] 
**sidecars** | **[Object]** |  | [optional] 
**container** | **Object** |  | [optional] 
**ports** | **[Number]** |  | [optional] 
**rewritePath** | **Boolean** | Rewrite path to remove polyaxon base url(i.e. /v1/services/namespace/owner/project/). Default is false, the service shoud handle a base url. | [optional] 



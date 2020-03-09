# PolyaxonSdk.V1Dask

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to 'dask']
**scale** | **Number** |  | [optional] 
**adapt_min** | **Number** |  | [optional] 
**adapt_max** | **Number** |  | [optional] 
**adapt_interval** | **String** |  | [optional] 
**environment** | [**V1Environment**](V1Environment.md) |  | [optional] 
**connections** | **[String]** |  | [optional] 
**volumes** | [**[V1Volume]**](V1Volume.md) | Volumes is a list of volumes that can be mounted. | [optional] 
**init** | [**[V1Init]**](V1Init.md) |  | [optional] 
**sidecars** | [**[V1Container]**](V1Container.md) |  | [optional] 
**container** | [**V1Container**](V1Container.md) |  | [optional] 





# V1Service


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  |  [optional]
**environment** | [**V1Environment**](V1Environment.md) |  |  [optional]
**connections** | **List&lt;String&gt;** |  |  [optional]
**volumes** | **List&lt;Object&gt;** | Volumes is a list of volumes that can be mounted. |  [optional]
**init** | [**List&lt;V1Init&gt;**](V1Init.md) |  |  [optional]
**sidecars** | **List&lt;Object&gt;** |  |  [optional]
**container** | **Object** |  |  [optional]
**ports** | **List&lt;Integer&gt;** |  |  [optional]
**rewritePath** | **Boolean** | Rewrite path to remove polyaxon base url(i.e. /v1/services/namespace/owner/project/). Default is false, the service shoud handle a base url. |  [optional]




# PolyaxonSdk.V1TruncationStoppingPolicy

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to &#39;truncation&#39;]
**percent** | **Number** | The percentage of runs to stop, at each evaluation interval. e.g. 1 - 99. | [optional] 
**evaluationInterval** | **Number** | Interval/Frequency for applying the policy. | [optional] 
**minInterval** | **Number** |  | [optional] 
**minSamples** | **Number** |  | [optional] 
**includeSucceeded** | **Boolean** |  | [optional] 



# PolyaxonSdk.V1TruncationStoppingPolicy

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  | [optional] [default to 'truncation']
**percent** | **Number** | The percentage of runs to stop, at each evaluation interval. e.g. 1 - 99. | [optional] 
**evaluation_interval** | **Number** | Interval/Frequency for applying the policy. | [optional] 
**min_interval** | **Number** |  | [optional] 
**min_samples** | **Number** |  | [optional] 
**include_succeeded** | **Boolean** |  | [optional] 



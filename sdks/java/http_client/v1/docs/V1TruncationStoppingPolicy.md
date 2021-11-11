

# V1TruncationStoppingPolicy

Early stopping with truncation stopping, this policy stops a percentage of all running runs at every evaluation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**kind** | **String** |  |  [optional]
**percent** | **Integer** | The percentage of runs to stop, at each evaluation interval. e.g. 1 - 99. |  [optional]
**evaluationInterval** | **Integer** | Interval/Frequency for applying the policy. |  [optional]
**minInterval** | **Integer** |  |  [optional]
**minSamples** | **Integer** |  |  [optional]
**includeSucceeded** | **Boolean** |  |  [optional]




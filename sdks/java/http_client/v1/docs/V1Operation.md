

# V1Operation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **Float** |  |  [optional]
**kind** | **String** |  |  [optional]
**name** | **String** |  |  [optional]
**description** | **String** |  |  [optional]
**tags** | **List&lt;String&gt;** |  |  [optional]
**presets** | **List&lt;String&gt;** |  |  [optional]
**queue** | **String** |  |  [optional]
**cache** | [**V1Cache**](V1Cache.md) |  |  [optional]
**termination** | [**V1Termination**](V1Termination.md) |  |  [optional]
**plugins** | [**V1Plugins**](V1Plugins.md) |  |  [optional]
**schedule** | **Object** |  |  [optional]
**events** | [**List&lt;V1EventTrigger&gt;**](V1EventTrigger.md) |  |  [optional]
**hooks** | [**List&lt;V1Hook&gt;**](V1Hook.md) |  |  [optional]
**dependencies** | **List&lt;String&gt;** |  |  [optional]
**trigger** | **V1TriggerPolicy** |  |  [optional]
**conditions** | **String** |  |  [optional]
**skipOnUpstreamSkip** | **Boolean** |  |  [optional]
**matrix** | **Object** |  |  [optional]
**joins** | [**Map&lt;String, V1Join&gt;**](V1Join.md) |  |  [optional]
**params** | [**Map&lt;String, V1Param&gt;**](V1Param.md) |  |  [optional]
**runPatch** | **Object** |  |  [optional]
**patchStrategy** | **V1PatchStrategy** |  |  [optional]
**isPreset** | **Boolean** |  |  [optional]
**isApproved** | **Boolean** |  |  [optional]
**template** | [**V1Template**](V1Template.md) |  |  [optional]
**build** | [**V1Build**](V1Build.md) |  |  [optional]
**cost** | **Float** |  |  [optional]
**pathRef** | **String** |  |  [optional]
**hubRef** | **String** |  |  [optional]
**dagRef** | **String** |  |  [optional]
**urlRef** | **String** |  |  [optional]
**component** | [**V1Component**](V1Component.md) |  |  [optional]




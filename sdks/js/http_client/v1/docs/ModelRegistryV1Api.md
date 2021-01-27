# PolyaxonSdk.ModelRegistryV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveModelRegistry**](ModelRegistryV1Api.md#archiveModelRegistry) | **POST** /api/v1/{owner}/registry/{name}/archive | Archive registry model
[**bookmarkModelRegistry**](ModelRegistryV1Api.md#bookmarkModelRegistry) | **POST** /api/v1/{owner}/registry/{name}/bookmark | Bookmark registry model
[**createModelRegistry**](ModelRegistryV1Api.md#createModelRegistry) | **POST** /api/v1/{owner}/registry/create | Create registry model
[**createModelVersion**](ModelRegistryV1Api.md#createModelVersion) | **POST** /api/v1/{owner}/registry/{model}/versions | Create model version
[**createModelVersionStage**](ModelRegistryV1Api.md#createModelVersionStage) | **POST** /api/v1/{owner}/registry/{entity}/versions/{name}/stages | Create new model version stage
[**deleteModelRegistry**](ModelRegistryV1Api.md#deleteModelRegistry) | **DELETE** /api/v1/{owner}/registry/{name} | Delete registry model
[**deleteModelVersion**](ModelRegistryV1Api.md#deleteModelVersion) | **DELETE** /api/v1/{owner}/registry/{entity}/versions/{name} | Delete model version
[**getModelRegistry**](ModelRegistryV1Api.md#getModelRegistry) | **GET** /api/v1/{owner}/registry/{name} | Get registry model
[**getModelRegistryActivities**](ModelRegistryV1Api.md#getModelRegistryActivities) | **GET** /api/v1/{owner}/registry/{name}/activities | Get model activities
[**getModelRegistrySettings**](ModelRegistryV1Api.md#getModelRegistrySettings) | **GET** /api/v1/{owner}/registry/{name}/settings | Get registry model settings
[**getModelVersion**](ModelRegistryV1Api.md#getModelVersion) | **GET** /api/v1/{owner}/registry/{entity}/versions/{name} | Get model version
[**getModelVersionStages**](ModelRegistryV1Api.md#getModelVersionStages) | **GET** /api/v1/{owner}/registry/{entity}/versions/{name}/stages | Get model version stages
[**listModelRegistries**](ModelRegistryV1Api.md#listModelRegistries) | **GET** /api/v1/{owner}/registry/list | List registry models
[**listModelRegistryNames**](ModelRegistryV1Api.md#listModelRegistryNames) | **GET** /api/v1/{owner}/registry/names | List registry model names
[**listModelVersionNames**](ModelRegistryV1Api.md#listModelVersionNames) | **GET** /api/v1/{owner}/registry/{name}/versions/names | List model versions names
[**listModelVersions**](ModelRegistryV1Api.md#listModelVersions) | **GET** /api/v1/{owner}/registry/{name}/versions | List model versions
[**patchModelRegistry**](ModelRegistryV1Api.md#patchModelRegistry) | **PATCH** /api/v1/{owner}/registry/{model.name} | Patch registry model
[**patchModelRegistrySettings**](ModelRegistryV1Api.md#patchModelRegistrySettings) | **PATCH** /api/v1/{owner}/registry/{model}/settings | Patch registry model settings
[**patchModelVersion**](ModelRegistryV1Api.md#patchModelVersion) | **PATCH** /api/v1/{owner}/registry/{model}/versions/{version.name} | Patch model version
[**restoreModelRegistry**](ModelRegistryV1Api.md#restoreModelRegistry) | **POST** /api/v1/{owner}/registry/{name}/restore | Restore registry model
[**unbookmarkModelRegistry**](ModelRegistryV1Api.md#unbookmarkModelRegistry) | **DELETE** /api/v1/{owner}/registry/{name}/unbookmark | Unbookmark registry model
[**updateModelRegistry**](ModelRegistryV1Api.md#updateModelRegistry) | **PUT** /api/v1/{owner}/registry/{model.name} | Update registry model
[**updateModelRegistrySettings**](ModelRegistryV1Api.md#updateModelRegistrySettings) | **PUT** /api/v1/{owner}/registry/{model}/settings | Update registry model settings
[**updateModelVersion**](ModelRegistryV1Api.md#updateModelVersion) | **PUT** /api/v1/{owner}/registry/{model}/versions/{version.name} | Update model version



## archiveModelRegistry

> archiveModelRegistry(owner, name)

Archive registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.archiveModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## bookmarkModelRegistry

> bookmarkModelRegistry(owner, name)

Bookmark registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.bookmarkModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## createModelRegistry

> V1ModelRegistry createModelRegistry(owner, body)

Create registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1ModelRegistry(); // V1ModelRegistry | Model body
apiInstance.createModelRegistry(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1ModelRegistry**](V1ModelRegistry.md)| Model body | 

### Return type

[**V1ModelRegistry**](V1ModelRegistry.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## createModelVersion

> V1ModelVersion createModelVersion(owner, model, body)

Create model version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model = "model_example"; // String | Model name
let body = new PolyaxonSdk.V1ModelVersion(); // V1ModelVersion | Model version body
apiInstance.createModelVersion(owner, model, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model** | **String**| Model name | 
 **body** | [**V1ModelVersion**](V1ModelVersion.md)| Model version body | 

### Return type

[**V1ModelVersion**](V1ModelVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## createModelVersionStage

> V1Stage createModelVersionStage(owner, entity, name, body)

Create new model version stage

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity namespace
let name = "name_example"; // String | Name of the version to apply the stage to
let body = new PolyaxonSdk.V1EntityStageBodyRequest(); // V1EntityStageBodyRequest | 
apiInstance.createModelVersionStage(owner, entity, name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **entity** | **String**| Entity namespace | 
 **name** | **String**| Name of the version to apply the stage to | 
 **body** | [**V1EntityStageBodyRequest**](V1EntityStageBodyRequest.md)|  | 

### Return type

[**V1Stage**](V1Stage.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteModelRegistry

> deleteModelRegistry(owner, name)

Delete registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.deleteModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## deleteModelVersion

> deleteModelVersion(owner, entity, name)

Delete model version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.deleteModelVersion(owner, entity, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **entity** | **String**| Entity: project name, hub name, registry name, ... | 
 **name** | **String**| Sub-entity name | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getModelRegistry

> V1ModelRegistry getModelRegistry(owner, name)

Get registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

[**V1ModelRegistry**](V1ModelRegistry.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getModelRegistryActivities

> V1ListActivitiesResponse getModelRegistryActivities(owner, name, opts)

Get model activities

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.getModelRegistryActivities(owner, name, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Entity managing the resource | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 

### Return type

[**V1ListActivitiesResponse**](V1ListActivitiesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getModelRegistrySettings

> V1ModelRegistrySettings getModelRegistrySettings(owner, name)

Get registry model settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getModelRegistrySettings(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

[**V1ModelRegistrySettings**](V1ModelRegistrySettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getModelVersion

> V1ModelVersion getModelVersion(owner, entity, name)

Get model version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.getModelVersion(owner, entity, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **entity** | **String**| Entity: project name, hub name, registry name, ... | 
 **name** | **String**| Sub-entity name | 

### Return type

[**V1ModelVersion**](V1ModelVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getModelVersionStages

> V1Stage getModelVersionStages(owner, entity, name)

Get model version stages

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.getModelVersionStages(owner, entity, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **entity** | **String**| Entity: project name, hub name, registry name, ... | 
 **name** | **String**| Sub-entity name | 

### Return type

[**V1Stage**](V1Stage.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listModelRegistries

> V1ListModelRegistriesResponse listModelRegistries(owner, opts)

List registry models

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listModelRegistries(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 

### Return type

[**V1ListModelRegistriesResponse**](V1ListModelRegistriesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listModelRegistryNames

> V1ListModelRegistriesResponse listModelRegistryNames(owner, opts)

List registry model names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listModelRegistryNames(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 

### Return type

[**V1ListModelRegistriesResponse**](V1ListModelRegistriesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listModelVersionNames

> V1ListModelVersionsResponse listModelVersionNames(owner, name, opts)

List model versions names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listModelVersionNames(owner, name, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Entity managing the resource | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 

### Return type

[**V1ListModelVersionsResponse**](V1ListModelVersionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listModelVersions

> V1ListModelVersionsResponse listModelVersions(owner, name, opts)

List model versions

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listModelVersions(owner, name, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Entity managing the resource | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 

### Return type

[**V1ListModelVersionsResponse**](V1ListModelVersionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchModelRegistry

> V1ModelRegistry patchModelRegistry(owner, model_name, body)

Patch registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model_name = "model_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ModelRegistry(); // V1ModelRegistry | Model body
apiInstance.patchModelRegistry(owner, model_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ModelRegistry**](V1ModelRegistry.md)| Model body | 

### Return type

[**V1ModelRegistry**](V1ModelRegistry.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchModelRegistrySettings

> V1ModelRegistrySettings patchModelRegistrySettings(owner, model, body)

Patch registry model settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model = "model_example"; // String | Model name
let body = new PolyaxonSdk.V1ModelRegistrySettings(); // V1ModelRegistrySettings | Model settings body
apiInstance.patchModelRegistrySettings(owner, model, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model** | **String**| Model name | 
 **body** | [**V1ModelRegistrySettings**](V1ModelRegistrySettings.md)| Model settings body | 

### Return type

[**V1ModelRegistrySettings**](V1ModelRegistrySettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchModelVersion

> V1ModelVersion patchModelVersion(owner, model, version_name, body)

Patch model version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model = "model_example"; // String | Model name
let version_name = "version_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ModelVersion(); // V1ModelVersion | Model version body
apiInstance.patchModelVersion(owner, model, version_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model** | **String**| Model name | 
 **version_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ModelVersion**](V1ModelVersion.md)| Model version body | 

### Return type

[**V1ModelVersion**](V1ModelVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## restoreModelRegistry

> restoreModelRegistry(owner, name)

Restore registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.restoreModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## unbookmarkModelRegistry

> unbookmarkModelRegistry(owner, name)

Unbookmark registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.unbookmarkModelRegistry(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## updateModelRegistry

> V1ModelRegistry updateModelRegistry(owner, model_name, body)

Update registry model

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model_name = "model_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ModelRegistry(); // V1ModelRegistry | Model body
apiInstance.updateModelRegistry(owner, model_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ModelRegistry**](V1ModelRegistry.md)| Model body | 

### Return type

[**V1ModelRegistry**](V1ModelRegistry.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateModelRegistrySettings

> V1ModelRegistrySettings updateModelRegistrySettings(owner, model, body)

Update registry model settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model = "model_example"; // String | Model name
let body = new PolyaxonSdk.V1ModelRegistrySettings(); // V1ModelRegistrySettings | Model settings body
apiInstance.updateModelRegistrySettings(owner, model, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model** | **String**| Model name | 
 **body** | [**V1ModelRegistrySettings**](V1ModelRegistrySettings.md)| Model settings body | 

### Return type

[**V1ModelRegistrySettings**](V1ModelRegistrySettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateModelVersion

> V1ModelVersion updateModelVersion(owner, model, version_name, body)

Update model version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ModelRegistryV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let model = "model_example"; // String | Model name
let version_name = "version_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ModelVersion(); // V1ModelVersion | Model version body
apiInstance.updateModelVersion(owner, model, version_name, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **model** | **String**| Model name | 
 **version_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ModelVersion**](V1ModelVersion.md)| Model version body | 

### Return type

[**V1ModelVersion**](V1ModelVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


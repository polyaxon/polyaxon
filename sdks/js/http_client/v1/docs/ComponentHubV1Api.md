# PolyaxonSdk.ComponentHubV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveComponentHub**](ComponentHubV1Api.md#archiveComponentHub) | **POST** /api/v1/{owner}/hub/{name}/archive | Archive hub component
[**bookmarkComponentHub**](ComponentHubV1Api.md#bookmarkComponentHub) | **POST** /api/v1/{owner}/hub/{name}/bookmark | Bookmark component hub
[**createComponentHub**](ComponentHubV1Api.md#createComponentHub) | **POST** /api/v1/{owner}/hub/create | Create hub component
[**createComponentVersion**](ComponentHubV1Api.md#createComponentVersion) | **POST** /api/v1/{owner}/hub/{component}/versions | Create component version
[**createComponentVersionStage**](ComponentHubV1Api.md#createComponentVersionStage) | **POST** /api/v1/{owner}/hub/{entity}/versions/{name}/stages | Create new component version stage
[**deleteComponentHub**](ComponentHubV1Api.md#deleteComponentHub) | **DELETE** /api/v1/{owner}/hub/{name} | Delete hub component
[**deleteComponentVersion**](ComponentHubV1Api.md#deleteComponentVersion) | **DELETE** /api/v1/{owner}/hub/{entity}/versions/{name} | Delete component version
[**getComponentHub**](ComponentHubV1Api.md#getComponentHub) | **GET** /api/v1/{owner}/hub/{name} | Get hub component
[**getComponentHubSettings**](ComponentHubV1Api.md#getComponentHubSettings) | **GET** /api/v1/{owner}/hub/{name}/settings | Get hub component settings
[**getComponentVersion**](ComponentHubV1Api.md#getComponentVersion) | **GET** /api/v1/{owner}/hub/{entity}/versions/{name} | Get component version
[**getComponentVersionStages**](ComponentHubV1Api.md#getComponentVersionStages) | **GET** /api/v1/{owner}/hub/{entity}/versions/{name}/stages | Get component version stages
[**listComponentHubNames**](ComponentHubV1Api.md#listComponentHubNames) | **GET** /api/v1/{owner}/hub/names | List hub component names
[**listComponentHubs**](ComponentHubV1Api.md#listComponentHubs) | **GET** /api/v1/{owner}/hub/list | List hub components
[**listComponentVersionNames**](ComponentHubV1Api.md#listComponentVersionNames) | **GET** /api/v1/{owner}/hub/{name}/versions/names | List component version names
[**listComponentVersions**](ComponentHubV1Api.md#listComponentVersions) | **GET** /api/v1/{owner}/hub/{name}/versions | List component versions
[**patchComponentHub**](ComponentHubV1Api.md#patchComponentHub) | **PATCH** /api/v1/{owner}/hub/{component.name} | Patch hub component
[**patchComponentHubSettings**](ComponentHubV1Api.md#patchComponentHubSettings) | **PATCH** /api/v1/{owner}/hub/{component}/settings | Patch hub component settings
[**patchComponentVersion**](ComponentHubV1Api.md#patchComponentVersion) | **PATCH** /api/v1/{owner}/hub/{component}/versions/{version.name} | Patch component version
[**restoreComponentHub**](ComponentHubV1Api.md#restoreComponentHub) | **POST** /api/v1/{owner}/hub/{name}/restore | Restore hub component
[**unbookmarkComponentHub**](ComponentHubV1Api.md#unbookmarkComponentHub) | **DELETE** /api/v1/{owner}/hub/{name}/unbookmark | Unbookmark component hub
[**updateComponentHub**](ComponentHubV1Api.md#updateComponentHub) | **PUT** /api/v1/{owner}/hub/{component.name} | Update hub component
[**updateComponentHubSettings**](ComponentHubV1Api.md#updateComponentHubSettings) | **PUT** /api/v1/{owner}/hub/{component}/settings | Update hub component settings
[**updateComponentVersion**](ComponentHubV1Api.md#updateComponentVersion) | **PUT** /api/v1/{owner}/hub/{component}/versions/{version.name} | Update component version



## archiveComponentHub

> archiveComponentHub(owner, name)

Archive hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.archiveComponentHub(owner, name, (error, data, response) => {
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


## bookmarkComponentHub

> bookmarkComponentHub(owner, name)

Bookmark component hub

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.bookmarkComponentHub(owner, name, (error, data, response) => {
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


## createComponentHub

> V1ComponentHub createComponentHub(owner, body)

Create hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1ComponentHub(); // V1ComponentHub | Component body
apiInstance.createComponentHub(owner, body, (error, data, response) => {
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
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body | 

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## createComponentVersion

> V1ComponentVersion createComponentVersion(owner, component, body)

Create component version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component = "component_example"; // String | Component name
let body = new PolyaxonSdk.V1ComponentVersion(); // V1ComponentVersion | Component version body
apiInstance.createComponentVersion(owner, component, body, (error, data, response) => {
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
 **component** | **String**| Component name | 
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body | 

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## createComponentVersionStage

> V1Stage createComponentVersionStage(owner, entity, name, body)

Create new component version stage

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity namespace
let name = "name_example"; // String | Name of the version to apply the stage to
let body = new PolyaxonSdk.V1EntityStageBodyRequest(); // V1EntityStageBodyRequest | 
apiInstance.createComponentVersionStage(owner, entity, name, body, (error, data, response) => {
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


## deleteComponentHub

> deleteComponentHub(owner, name)

Delete hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.deleteComponentHub(owner, name, (error, data, response) => {
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


## deleteComponentVersion

> deleteComponentVersion(owner, entity, name)

Delete component version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.deleteComponentVersion(owner, entity, name, (error, data, response) => {
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


## getComponentHub

> V1ComponentHub getComponentHub(owner, name)

Get hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getComponentHub(owner, name, (error, data, response) => {
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

[**V1ComponentHub**](V1ComponentHub.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getComponentHubSettings

> V1ComponentHubSettings getComponentHubSettings(owner, name)

Get hub component settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getComponentHubSettings(owner, name, (error, data, response) => {
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

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getComponentVersion

> V1ComponentVersion getComponentVersion(owner, entity, name)

Get component version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.getComponentVersion(owner, entity, name, (error, data, response) => {
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

[**V1ComponentVersion**](V1ComponentVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getComponentVersionStages

> V1Stage getComponentVersionStages(owner, entity, name)

Get component version stages

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let entity = "entity_example"; // String | Entity: project name, hub name, registry name, ...
let name = "name_example"; // String | Sub-entity name
apiInstance.getComponentVersionStages(owner, entity, name, (error, data, response) => {
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


## listComponentHubNames

> V1ListComponentHubsResponse listComponentHubNames(owner, opts)

List hub component names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listComponentHubNames(owner, opts, (error, data, response) => {
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

[**V1ListComponentHubsResponse**](V1ListComponentHubsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listComponentHubs

> V1ListComponentHubsResponse listComponentHubs(owner, opts)

List hub components

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listComponentHubs(owner, opts, (error, data, response) => {
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

[**V1ListComponentHubsResponse**](V1ListComponentHubsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listComponentVersionNames

> V1ListComponentVersionsResponse listComponentVersionNames(owner, name, opts)

List component version names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listComponentVersionNames(owner, name, opts, (error, data, response) => {
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

[**V1ListComponentVersionsResponse**](V1ListComponentVersionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listComponentVersions

> V1ListComponentVersionsResponse listComponentVersions(owner, name, opts)

List component versions

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search.
};
apiInstance.listComponentVersions(owner, name, opts, (error, data, response) => {
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

[**V1ListComponentVersionsResponse**](V1ListComponentVersionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchComponentHub

> V1ComponentHub patchComponentHub(owner, component_name, body)

Patch hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component_name = "component_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ComponentHub(); // V1ComponentHub | Component body
apiInstance.patchComponentHub(owner, component_name, body, (error, data, response) => {
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
 **component_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body | 

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchComponentHubSettings

> V1ComponentHubSettings patchComponentHubSettings(owner, component, body)

Patch hub component settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component = "component_example"; // String | Hub name
let body = new PolyaxonSdk.V1ComponentHubSettings(); // V1ComponentHubSettings | Hub settings body
apiInstance.patchComponentHubSettings(owner, component, body, (error, data, response) => {
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
 **component** | **String**| Hub name | 
 **body** | [**V1ComponentHubSettings**](V1ComponentHubSettings.md)| Hub settings body | 

### Return type

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchComponentVersion

> V1ComponentVersion patchComponentVersion(owner, component, version_name, body)

Patch component version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component = "component_example"; // String | Component name
let version_name = "version_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ComponentVersion(); // V1ComponentVersion | Component version body
apiInstance.patchComponentVersion(owner, component, version_name, body, (error, data, response) => {
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
 **component** | **String**| Component name | 
 **version_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body | 

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## restoreComponentHub

> restoreComponentHub(owner, name)

Restore hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.restoreComponentHub(owner, name, (error, data, response) => {
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


## unbookmarkComponentHub

> unbookmarkComponentHub(owner, name)

Unbookmark component hub

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.unbookmarkComponentHub(owner, name, (error, data, response) => {
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


## updateComponentHub

> V1ComponentHub updateComponentHub(owner, component_name, body)

Update hub component

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component_name = "component_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ComponentHub(); // V1ComponentHub | Component body
apiInstance.updateComponentHub(owner, component_name, body, (error, data, response) => {
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
 **component_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ComponentHub**](V1ComponentHub.md)| Component body | 

### Return type

[**V1ComponentHub**](V1ComponentHub.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateComponentHubSettings

> V1ComponentHubSettings updateComponentHubSettings(owner, component, body)

Update hub component settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component = "component_example"; // String | Hub name
let body = new PolyaxonSdk.V1ComponentHubSettings(); // V1ComponentHubSettings | Hub settings body
apiInstance.updateComponentHubSettings(owner, component, body, (error, data, response) => {
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
 **component** | **String**| Hub name | 
 **body** | [**V1ComponentHubSettings**](V1ComponentHubSettings.md)| Hub settings body | 

### Return type

[**V1ComponentHubSettings**](V1ComponentHubSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateComponentVersion

> V1ComponentVersion updateComponentVersion(owner, component, version_name, body)

Update component version

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ComponentHubV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let component = "component_example"; // String | Component name
let version_name = "version_name_example"; // String | Optional component name, should be a valid fully qualified value: name[:version]
let body = new PolyaxonSdk.V1ComponentVersion(); // V1ComponentVersion | Component version body
apiInstance.updateComponentVersion(owner, component, version_name, body, (error, data, response) => {
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
 **component** | **String**| Component name | 
 **version_name** | **String**| Optional component name, should be a valid fully qualified value: name[:version] | 
 **body** | [**V1ComponentVersion**](V1ComponentVersion.md)| Component version body | 

### Return type

[**V1ComponentVersion**](V1ComponentVersion.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


# PolyaxonSdk.ArtifactsStoresV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createArtifactsStore**](ArtifactsStoresV1Api.md#createArtifactsStore) | **POST** /api/v1/{owner}/artifacts_stores | List runs
[**deleteArtifactsStore**](ArtifactsStoresV1Api.md#deleteArtifactsStore) | **DELETE** /api/v1/{owner}/artifacts_stores/{uuid} | Patch run
[**getArtifactsStore**](ArtifactsStoresV1Api.md#getArtifactsStore) | **GET** /api/v1/{owner}/artifacts_stores/{uuid} | Create new run
[**listArtifactsStoreNames**](ArtifactsStoresV1Api.md#listArtifactsStoreNames) | **GET** /api/v1/{owner}/artifacts_stores/names | List bookmarked runs for user
[**listArtifactsStores**](ArtifactsStoresV1Api.md#listArtifactsStores) | **GET** /api/v1/{owner}/artifacts_stores | List archived runs for user
[**patchArtifactsStore**](ArtifactsStoresV1Api.md#patchArtifactsStore) | **PATCH** /api/v1/{owner}/artifacts_stores/{artifact_store.uuid} | Update run
[**updateArtifactsStore**](ArtifactsStoresV1Api.md#updateArtifactsStore) | **PUT** /api/v1/{owner}/artifacts_stores/{artifact_store.uuid} | Get run


<a name="createArtifactsStore"></a>
# **createArtifactsStore**
> V1ArtifactsStore createArtifactsStore(owner, body)

List runs

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createArtifactsStore(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body | 

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteArtifactsStore"></a>
# **deleteArtifactsStore**
> Object deleteArtifactsStore(owner, uuid)

Patch run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteArtifactsStore(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getArtifactsStore"></a>
# **getArtifactsStore**
> V1ArtifactsStore getArtifactsStore(owner, uuid)

Create new run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getArtifactsStore(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArtifactsStoreNames"></a>
# **listArtifactsStoreNames**
> V1ListArtifactsStoresResponse listArtifactsStoreNames(owner, opts)

List bookmarked runs for user

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArtifactsStoreNames(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListArtifactsStoresResponse**](V1ListArtifactsStoresResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArtifactsStores"></a>
# **listArtifactsStores**
> V1ListArtifactsStoresResponse listArtifactsStores(owner, opts)

List archived runs for user

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var opts = { 
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArtifactsStores(owner, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListArtifactsStoresResponse**](V1ListArtifactsStoresResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchArtifactsStore"></a>
# **patchArtifactsStore**
> V1ArtifactsStore patchArtifactsStore(owner, artifact_store_uuid, body)

Update run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var artifact_store_uuid = "artifact_store_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchArtifactsStore(owner, artifact_store_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **artifact_store_uuid** | **String**| UUID | 
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body | 

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateArtifactsStore"></a>
# **updateArtifactsStore**
> V1ArtifactsStore updateArtifactsStore(owner, artifact_store_uuid, body)

Get run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ArtifactsStoresV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var artifact_store_uuid = "artifact_store_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1ArtifactsStore(); // V1ArtifactsStore | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateArtifactsStore(owner, artifact_store_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **artifact_store_uuid** | **String**| UUID | 
 **body** | [**V1ArtifactsStore**](V1ArtifactsStore.md)| Artifact store body | 

### Return type

[**V1ArtifactsStore**](V1ArtifactsStore.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


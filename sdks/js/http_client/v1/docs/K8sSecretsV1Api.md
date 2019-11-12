# PolyaxonSdk.K8sSecretsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8sSecrets**](K8sSecretsV1Api.md#createK8sSecrets) | **POST** /api/v1/{owner}/k8s_secrets | List runs
[**deleteK8sSecret**](K8sSecretsV1Api.md#deleteK8sSecret) | **DELETE** /api/v1/{owner}/k8s_secrets/{uuid} | Patch run
[**getK8sSecret**](K8sSecretsV1Api.md#getK8sSecret) | **GET** /api/v1/{owner}/k8s_secrets/{uuid} | Create new run
[**listK8sSecretNames**](K8sSecretsV1Api.md#listK8sSecretNames) | **GET** /api/v1/{owner}/k8s_secrets/names | List bookmarked runs for user
[**listK8sSecrets**](K8sSecretsV1Api.md#listK8sSecrets) | **GET** /api/v1/{owner}/k8s_secrets | List archived runs for user
[**patchK8sSecret**](K8sSecretsV1Api.md#patchK8sSecret) | **PATCH** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Update run
[**updateK8sSecret**](K8sSecretsV1Api.md#updateK8sSecret) | **PUT** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Get run


<a name="createK8sSecrets"></a>
# **createK8sSecrets**
> V1K8sResource createK8sSecrets(owner, body)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1K8sResource(); // V1K8sResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createK8sSecrets(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8sSecret"></a>
# **deleteK8sSecret**
> deleteK8sSecret(owner, uuid)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.deleteK8sSecret(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getK8sSecret"></a>
# **getK8sSecret**
> V1K8sResource getK8sSecret(owner, uuid)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getK8sSecret(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sSecretNames"></a>
# **listK8sSecretNames**
> V1ListK8sResourcesResponse listK8sSecretNames(owner, opts)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

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
apiInstance.listK8sSecretNames(owner, opts, callback);
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sSecrets"></a>
# **listK8sSecrets**
> V1ListK8sResourcesResponse listK8sSecrets(owner, opts)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

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
apiInstance.listK8sSecrets(owner, opts, callback);
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8sSecret"></a>
# **patchK8sSecret**
> V1K8sResource patchK8sSecret(owner, k8s_resource_uuid, body)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var k8s_resource_uuid = "k8s_resource_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1K8sResource(); // V1K8sResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchK8sSecret(owner, k8s_resource_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **k8s_resource_uuid** | **String**| UUID | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8sSecret"></a>
# **updateK8sSecret**
> V1K8sResource updateK8sSecret(owner, k8s_resource_uuid, body)

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

var apiInstance = new PolyaxonSdk.K8sSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var k8s_resource_uuid = "k8s_resource_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1K8sResource(); // V1K8sResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateK8sSecret(owner, k8s_resource_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **k8s_resource_uuid** | **String**| UUID | 
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body | 

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


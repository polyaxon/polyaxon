# PolyaxonSdk.K8SSecretsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8SSecrets**](K8SSecretsV1Api.md#createK8SSecrets) | **POST** /api/v1/{owner}/k8s_secrets | List runs
[**deleteK8SSecret**](K8SSecretsV1Api.md#deleteK8SSecret) | **DELETE** /api/v1/{owner}/k8s_secrets/{uuid} | Patch run
[**getK8SSecret**](K8SSecretsV1Api.md#getK8SSecret) | **GET** /api/v1/{owner}/k8s_secrets/{uuid} | Create new run
[**listK8SSecretNames**](K8SSecretsV1Api.md#listK8SSecretNames) | **GET** /api/v1/{owner}/k8s_secrets/names | List bookmarked runs for user
[**listK8SSecrets**](K8SSecretsV1Api.md#listK8SSecrets) | **GET** /api/v1/{owner}/k8s_secrets | List archived runs for user
[**patchK8SSecret**](K8SSecretsV1Api.md#patchK8SSecret) | **PATCH** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Update run
[**updateK8SSecret**](K8SSecretsV1Api.md#updateK8SSecret) | **PUT** /api/v1/{owner}/k8s_secrets/{k8s_resource.uuid} | Get run


<a name="createK8SSecrets"></a>
# **createK8SSecrets**
> V1K8SResource createK8SSecrets(owner, body)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1K8SResource(); // V1K8SResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createK8SSecrets(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body | 

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8SSecret"></a>
# **deleteK8SSecret**
> Object deleteK8SSecret(owner, uuid)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteK8SSecret(owner, uuid, callback);
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

<a name="getK8SSecret"></a>
# **getK8SSecret**
> V1K8SResource getK8SSecret(owner, uuid)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getK8SSecret(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SSecretNames"></a>
# **listK8SSecretNames**
> V1ListK8SResourcesResponse listK8SSecretNames(owner, opts)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

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
apiInstance.listK8SSecretNames(owner, opts, callback);
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SSecrets"></a>
# **listK8SSecrets**
> V1ListK8SResourcesResponse listK8SSecrets(owner, opts)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

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
apiInstance.listK8SSecrets(owner, opts, callback);
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8SSecret"></a>
# **patchK8SSecret**
> V1K8SResource patchK8SSecret(owner, k8s_resource_uuid, body)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var k8s_resource_uuid = "k8s_resource_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1K8SResource(); // V1K8SResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchK8SSecret(owner, k8s_resource_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **k8s_resource_uuid** | **String**| UUID | 
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body | 

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8SSecret"></a>
# **updateK8SSecret**
> V1K8SResource updateK8SSecret(owner, k8s_resource_uuid, body)

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

var apiInstance = new PolyaxonSdk.K8SSecretsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var k8s_resource_uuid = "k8s_resource_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1K8SResource(); // V1K8SResource | Artifact store body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateK8SSecret(owner, k8s_resource_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **k8s_resource_uuid** | **String**| UUID | 
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body | 

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


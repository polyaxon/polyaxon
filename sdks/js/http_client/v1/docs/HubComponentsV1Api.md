# PolyaxonSdk.HubComponentsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**hubComponentsV1CreateHubComponent**](HubComponentsV1Api.md#hubComponentsV1CreateHubComponent) | **POST** /api/v1/orgs/{owner}/components | Create hub model
[**hubComponentsV1DeleteHubComponent**](HubComponentsV1Api.md#hubComponentsV1DeleteHubComponent) | **DELETE** /api/v1/orgs/{owner}/components/{uuid} | Delete hub model
[**hubComponentsV1GetHubComponent**](HubComponentsV1Api.md#hubComponentsV1GetHubComponent) | **GET** /api/v1/orgs/{owner}/components/{uuid} | Get hub model
[**hubComponentsV1ListHubComponebtNames**](HubComponentsV1Api.md#hubComponentsV1ListHubComponebtNames) | **GET** /api/v1/orgs/{owner}/components/names | List hub model names
[**hubComponentsV1ListHubComponents**](HubComponentsV1Api.md#hubComponentsV1ListHubComponents) | **GET** /api/v1/orgs/{owner}/components | List hub models
[**hubComponentsV1PatchHubComponent**](HubComponentsV1Api.md#hubComponentsV1PatchHubComponent) | **PATCH** /api/v1/orgs/{owner}/components/{component.uuid} | Patch hub model
[**hubComponentsV1UpdateHubComponent**](HubComponentsV1Api.md#hubComponentsV1UpdateHubComponent) | **PUT** /api/v1/orgs/{owner}/components/{component.uuid} | Update hub model


<a name="hubComponentsV1CreateHubComponent"></a>
# **hubComponentsV1CreateHubComponent**
> V1HubComponent hubComponentsV1CreateHubComponent(owner, body)

Create hub model

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1HubComponent(); // V1HubComponent | Component body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.hubComponentsV1CreateHubComponent(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1DeleteHubComponent"></a>
# **hubComponentsV1DeleteHubComponent**
> hubComponentsV1DeleteHubComponent(owner, uuid)

Delete hub model

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.hubComponentsV1DeleteHubComponent(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1GetHubComponent"></a>
# **hubComponentsV1GetHubComponent**
> V1HubComponent hubComponentsV1GetHubComponent(owner, uuid)

Get hub model

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.hubComponentsV1GetHubComponent(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1ListHubComponebtNames"></a>
# **hubComponentsV1ListHubComponebtNames**
> V1ListHubComponentsResponse hubComponentsV1ListHubComponebtNames(owner, opts)

List hub model names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

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
apiInstance.hubComponentsV1ListHubComponebtNames(owner, opts, callback);
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1ListHubComponents"></a>
# **hubComponentsV1ListHubComponents**
> V1ListHubComponentsResponse hubComponentsV1ListHubComponents(owner, opts)

List hub models

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

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
apiInstance.hubComponentsV1ListHubComponents(owner, opts, callback);
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

[**V1ListHubComponentsResponse**](V1ListHubComponentsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1PatchHubComponent"></a>
# **hubComponentsV1PatchHubComponent**
> V1HubComponent hubComponentsV1PatchHubComponent(owner, component_uuid, body)

Patch hub model

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var component_uuid = "component_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1HubComponent(); // V1HubComponent | Component body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.hubComponentsV1PatchHubComponent(owner, component_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **component_uuid** | **String**| UUID | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="hubComponentsV1UpdateHubComponent"></a>
# **hubComponentsV1UpdateHubComponent**
> V1HubComponent hubComponentsV1UpdateHubComponent(owner, component_uuid, body)

Update hub model

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.HubComponentsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var component_uuid = "component_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1HubComponent(); // V1HubComponent | Component body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.hubComponentsV1UpdateHubComponent(owner, component_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **component_uuid** | **String**| UUID | 
 **body** | [**V1HubComponent**](V1HubComponent.md)| Component body | 

### Return type

[**V1HubComponent**](V1HubComponent.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


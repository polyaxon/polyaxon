# PolyaxonSdk.ConnectionsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**connectionsV1CreateConnection**](ConnectionsV1Api.md#connectionsV1CreateConnection) | **POST** /api/v1/orgs/{owner}/connections | Create connection
[**connectionsV1DeleteConnection**](ConnectionsV1Api.md#connectionsV1DeleteConnection) | **DELETE** /api/v1/orgs/{owner}/connections/{uuid} | Delete connection
[**connectionsV1GetConnection**](ConnectionsV1Api.md#connectionsV1GetConnection) | **GET** /api/v1/orgs/{owner}/connections/{uuid} | Get connection
[**connectionsV1ListConnectionNames**](ConnectionsV1Api.md#connectionsV1ListConnectionNames) | **GET** /api/v1/orgs/{owner}/connections/names | List connections names
[**connectionsV1ListConnections**](ConnectionsV1Api.md#connectionsV1ListConnections) | **GET** /api/v1/orgs/{owner}/connections | List connections
[**connectionsV1PatchConnection**](ConnectionsV1Api.md#connectionsV1PatchConnection) | **PATCH** /api/v1/orgs/{owner}/connections/{connection.uuid} | Patch connection
[**connectionsV1UpdateConnection**](ConnectionsV1Api.md#connectionsV1UpdateConnection) | **PUT** /api/v1/orgs/{owner}/connections/{connection.uuid} | Update connection


<a name="connectionsV1CreateConnection"></a>
# **connectionsV1CreateConnection**
> V1ConnectionResponse connectionsV1CreateConnection(owner, body)

Create connection

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1ConnectionResponse(); // V1ConnectionResponse | Connection body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.connectionsV1CreateConnection(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1DeleteConnection"></a>
# **connectionsV1DeleteConnection**
> connectionsV1DeleteConnection(owner, uuid)

Delete connection

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.connectionsV1DeleteConnection(owner, uuid, callback);
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

<a name="connectionsV1GetConnection"></a>
# **connectionsV1GetConnection**
> V1ConnectionResponse connectionsV1GetConnection(owner, uuid)

Get connection

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.connectionsV1GetConnection(owner, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1ListConnectionNames"></a>
# **connectionsV1ListConnectionNames**
> V1ListConnectionsResponse connectionsV1ListConnectionNames(owner, opts)

List connections names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

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
apiInstance.connectionsV1ListConnectionNames(owner, opts, callback);
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1ListConnections"></a>
# **connectionsV1ListConnections**
> V1ListConnectionsResponse connectionsV1ListConnections(owner, opts)

List connections

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

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
apiInstance.connectionsV1ListConnections(owner, opts, callback);
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

[**V1ListConnectionsResponse**](V1ListConnectionsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1PatchConnection"></a>
# **connectionsV1PatchConnection**
> V1ConnectionResponse connectionsV1PatchConnection(owner, connection_uuid, body)

Patch connection

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var connection_uuid = "connection_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1ConnectionResponse(); // V1ConnectionResponse | Connection body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.connectionsV1PatchConnection(owner, connection_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **connection_uuid** | **String**| UUID | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="connectionsV1UpdateConnection"></a>
# **connectionsV1UpdateConnection**
> V1ConnectionResponse connectionsV1UpdateConnection(owner, connection_uuid, body)

Update connection

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ConnectionsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var connection_uuid = "connection_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1ConnectionResponse(); // V1ConnectionResponse | Connection body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.connectionsV1UpdateConnection(owner, connection_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **connection_uuid** | **String**| UUID | 
 **body** | [**V1ConnectionResponse**](V1ConnectionResponse.md)| Connection body | 

### Return type

[**V1ConnectionResponse**](V1ConnectionResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


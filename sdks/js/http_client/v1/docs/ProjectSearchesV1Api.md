# PolyaxonSdk.ProjectSearchesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createProjectSearch**](ProjectSearchesV1Api.md#createProjectSearch) | **POST** /api/v1/{owner}/{project}/searches | Create project search
[**deleteProjectSearch**](ProjectSearchesV1Api.md#deleteProjectSearch) | **DELETE** /api/v1/{owner}/{project}/searches/{uuid} | Delete project search
[**getProjectSearch**](ProjectSearchesV1Api.md#getProjectSearch) | **GET** /api/v1/{owner}/{project}/searches/{uuid} | Get project search
[**listProjectSearchNames**](ProjectSearchesV1Api.md#listProjectSearchNames) | **GET** /api/v1/{owner}/{project}/searches/names | List project search names
[**listProjectSearches**](ProjectSearchesV1Api.md#listProjectSearches) | **GET** /api/v1/{owner}/{project}/searches | List project searches
[**patchProjectSearch**](ProjectSearchesV1Api.md#patchProjectSearch) | **PATCH** /api/v1/{owner}/{project}/searches/{search.uuid} | Patch project search
[**promoteProjectSearch**](ProjectSearchesV1Api.md#promoteProjectSearch) | **POST** /api/v1/{owner}/{project}/searches/{uuid}/promote | Promote project search
[**updateProjectSearch**](ProjectSearchesV1Api.md#updateProjectSearch) | **PUT** /api/v1/{owner}/{project}/searches/{search.uuid} | Update project search


<a name="createProjectSearch"></a>
# **createProjectSearch**
> V1Search createProjectSearch(owner, project, body)

Create project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1Search(); // V1Search | Search body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createProjectSearch(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Search**](V1Search.md)| Search body | 

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteProjectSearch"></a>
# **deleteProjectSearch**
> deleteProjectSearch(owner, project, uuid)

Delete project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.deleteProjectSearch(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getProjectSearch"></a>
# **getProjectSearch**
> V1Search getProjectSearch(owner, project, uuid)

Get project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getProjectSearch(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectSearchNames"></a>
# **listProjectSearchNames**
> V1ListSearchesResponse listProjectSearchNames(owner, project, opts)

List project search names

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

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
apiInstance.listProjectSearchNames(owner, project, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectSearches"></a>
# **listProjectSearches**
> V1ListSearchesResponse listProjectSearches(owner, project, opts)

List project searches

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

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
apiInstance.listProjectSearches(owner, project, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchProjectSearch"></a>
# **patchProjectSearch**
> V1Search patchProjectSearch(owner, project, search_uuid, body)

Patch project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var search_uuid = "search_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Search(); // V1Search | Search body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchProjectSearch(owner, project, search_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **search_uuid** | **String**| UUID | 
 **body** | [**V1Search**](V1Search.md)| Search body | 

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="promoteProjectSearch"></a>
# **promoteProjectSearch**
> promoteProjectSearch(owner, project, uuid)

Promote project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.promoteProjectSearch(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateProjectSearch"></a>
# **updateProjectSearch**
> V1Search updateProjectSearch(owner, project, search_uuid, body)

Update project search

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectSearchesV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var search_uuid = "search_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Search(); // V1Search | Search body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateProjectSearch(owner, project, search_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **search_uuid** | **String**| UUID | 
 **body** | [**V1Search**](V1Search.md)| Search body | 

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


# PolyaxonSdk.ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createProjectDashboard**](ProjectDashboardsV1Api.md#createProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards | List runs
[**deleteProjectDashboard**](ProjectDashboardsV1Api.md#deleteProjectDashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Patch run
[**getProjectDashboard**](ProjectDashboardsV1Api.md#getProjectDashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Create new run
[**listProjectDashboardNames**](ProjectDashboardsV1Api.md#listProjectDashboardNames) | **GET** /api/v1/{owner}/{project}/dashboards/names | List bookmarked runs for user
[**listProjectDashboards**](ProjectDashboardsV1Api.md#listProjectDashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List archived runs for user
[**patchProjectDashboard**](ProjectDashboardsV1Api.md#patchProjectDashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update run
[**promoteProjectDashboard**](ProjectDashboardsV1Api.md#promoteProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Delete run
[**updateProjectDashboard**](ProjectDashboardsV1Api.md#updateProjectDashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Get run


<a name="createProjectDashboard"></a>
# **createProjectDashboard**
> V1Dashboard createProjectDashboard(owner, project, body)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createProjectDashboard(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteProjectDashboard"></a>
# **deleteProjectDashboard**
> deleteProjectDashboard(owner, project, uuid)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.deleteProjectDashboard(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getProjectDashboard"></a>
# **getProjectDashboard**
> V1Dashboard getProjectDashboard(owner, project, uuid)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getProjectDashboard(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectDashboardNames"></a>
# **listProjectDashboardNames**
> V1ListDashboardsResponse listProjectDashboardNames(owner, project, opts)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

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
apiInstance.listProjectDashboardNames(owner, project, opts, callback);
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectDashboards"></a>
# **listProjectDashboards**
> V1ListDashboardsResponse listProjectDashboards(owner, project, opts)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

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
apiInstance.listProjectDashboards(owner, project, opts, callback);
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchProjectDashboard"></a>
# **patchProjectDashboard**
> V1Dashboard patchProjectDashboard(owner, project, dashboard_uuid, body)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var dashboard_uuid = "dashboard_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchProjectDashboard(owner, project, dashboard_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **dashboard_uuid** | **String**| UUID | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="promoteProjectDashboard"></a>
# **promoteProjectDashboard**
> V1Dashboard promoteProjectDashboard(owner, project, dashboard_uuid)

Delete run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var dashboard_uuid = "dashboard_uuid_example"; // String | UUID


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.promoteProjectDashboard(owner, project, dashboard_uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **dashboard_uuid** | **String**| UUID | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateProjectDashboard"></a>
# **updateProjectDashboard**
> V1Dashboard updateProjectDashboard(owner, project, dashboard_uuid, body)

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

var apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var dashboard_uuid = "dashboard_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateProjectDashboard(owner, project, dashboard_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **dashboard_uuid** | **String**| UUID | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


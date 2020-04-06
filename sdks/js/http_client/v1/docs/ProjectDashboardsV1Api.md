# PolyaxonSdk.ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projectDashboardsV1CreateProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1CreateProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards | Create project dashboard
[**projectDashboardsV1DeleteProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1DeleteProjectDashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Delete project dashboard
[**projectDashboardsV1GetProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1GetProjectDashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Get project dashboard
[**projectDashboardsV1ListProjectDashboardNames**](ProjectDashboardsV1Api.md#projectDashboardsV1ListProjectDashboardNames) | **GET** /api/v1/{owner}/{project}/dashboards/names | List project dashboard
[**projectDashboardsV1ListProjectDashboards**](ProjectDashboardsV1Api.md#projectDashboardsV1ListProjectDashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List project dashboards
[**projectDashboardsV1PatchProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1PatchProjectDashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Patch project dashboard
[**projectDashboardsV1PromoteProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1PromoteProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Promote project dashboard
[**projectDashboardsV1UpdateProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1UpdateProjectDashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update project dashboard


<a name="projectDashboardsV1CreateProjectDashboard"></a>
# **projectDashboardsV1CreateProjectDashboard**
> V1Dashboard projectDashboardsV1CreateProjectDashboard(owner, project, body)

Create project dashboard

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
apiInstance.projectDashboardsV1CreateProjectDashboard(owner, project, body, callback);
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

<a name="projectDashboardsV1DeleteProjectDashboard"></a>
# **projectDashboardsV1DeleteProjectDashboard**
> projectDashboardsV1DeleteProjectDashboard(owner, project, uuid)

Delete project dashboard

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.projectDashboardsV1DeleteProjectDashboard(owner, project, uuid, callback);
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

<a name="projectDashboardsV1GetProjectDashboard"></a>
# **projectDashboardsV1GetProjectDashboard**
> V1Dashboard projectDashboardsV1GetProjectDashboard(owner, project, uuid)

Get project dashboard

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.projectDashboardsV1GetProjectDashboard(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1ListProjectDashboardNames"></a>
# **projectDashboardsV1ListProjectDashboardNames**
> V1ListDashboardsResponse projectDashboardsV1ListProjectDashboardNames(owner, project, opts)

List project dashboard

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
apiInstance.projectDashboardsV1ListProjectDashboardNames(owner, project, opts, callback);
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

<a name="projectDashboardsV1ListProjectDashboards"></a>
# **projectDashboardsV1ListProjectDashboards**
> V1ListDashboardsResponse projectDashboardsV1ListProjectDashboards(owner, project, opts)

List project dashboards

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
apiInstance.projectDashboardsV1ListProjectDashboards(owner, project, opts, callback);
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

<a name="projectDashboardsV1PatchProjectDashboard"></a>
# **projectDashboardsV1PatchProjectDashboard**
> V1Dashboard projectDashboardsV1PatchProjectDashboard(owner, project, dashboard_uuid, body)

Patch project dashboard

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
apiInstance.projectDashboardsV1PatchProjectDashboard(owner, project, dashboard_uuid, body, callback);
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

<a name="projectDashboardsV1PromoteProjectDashboard"></a>
# **projectDashboardsV1PromoteProjectDashboard**
> V1Dashboard projectDashboardsV1PromoteProjectDashboard(owner, project, dashboard_uuid)

Promote project dashboard

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
apiInstance.projectDashboardsV1PromoteProjectDashboard(owner, project, dashboard_uuid, callback);
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

<a name="projectDashboardsV1UpdateProjectDashboard"></a>
# **projectDashboardsV1UpdateProjectDashboard**
> V1Dashboard projectDashboardsV1UpdateProjectDashboard(owner, project, dashboard_uuid, body)

Update project dashboard

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
apiInstance.projectDashboardsV1UpdateProjectDashboard(owner, project, dashboard_uuid, body, callback);
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


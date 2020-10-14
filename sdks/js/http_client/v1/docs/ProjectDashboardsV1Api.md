# PolyaxonSdk.ProjectDashboardsV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createProjectDashboard**](ProjectDashboardsV1Api.md#createProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards | Create project dashboard
[**deleteProjectDashboard**](ProjectDashboardsV1Api.md#deleteProjectDashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Delete project dashboard
[**getProjectDashboard**](ProjectDashboardsV1Api.md#getProjectDashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Get project dashboard
[**listProjectDashboardNames**](ProjectDashboardsV1Api.md#listProjectDashboardNames) | **GET** /api/v1/{owner}/{project}/dashboards/names | List project dashboard
[**listProjectDashboards**](ProjectDashboardsV1Api.md#listProjectDashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List project dashboards
[**patchProjectDashboard**](ProjectDashboardsV1Api.md#patchProjectDashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Patch project dashboard
[**promoteProjectDashboard**](ProjectDashboardsV1Api.md#promoteProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{uuid}/promote | Promote project dashboard
[**updateProjectDashboard**](ProjectDashboardsV1Api.md#updateProjectDashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update project dashboard



## createProjectDashboard

> V1Dashboard createProjectDashboard(owner, project, body)

Create project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project under namesapce
let body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body
apiInstance.createProjectDashboard(owner, project, body, (error, data, response) => {
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
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteProjectDashboard

> Object deleteProjectDashboard(owner, project, uuid)

Delete project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project
let uuid = "uuid_example"; // String | Uuid identifier of the entity
apiInstance.deleteProjectDashboard(owner, project, uuid, (error, data, response) => {
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
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProjectDashboard

> V1Dashboard getProjectDashboard(owner, project, uuid)

Get project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project
let uuid = "uuid_example"; // String | Uuid identifier of the entity
apiInstance.getProjectDashboard(owner, project, uuid, (error, data, response) => {
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
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProjectDashboardNames

> V1ListDashboardsResponse listProjectDashboardNames(owner, project, opts)

List project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project under namesapce
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listProjectDashboardNames(owner, project, opts, (error, data, response) => {
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

- **Content-Type**: Not defined
- **Accept**: application/json


## listProjectDashboards

> V1ListDashboardsResponse listProjectDashboards(owner, project, opts)

List project dashboards

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project under namesapce
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example" // String | Query filter the search search.
};
apiInstance.listProjectDashboards(owner, project, opts, (error, data, response) => {
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

- **Content-Type**: Not defined
- **Accept**: application/json


## patchProjectDashboard

> V1Dashboard patchProjectDashboard(owner, project, dashboard_uuid, body)

Patch project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project under namesapce
let dashboard_uuid = "dashboard_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body
apiInstance.patchProjectDashboard(owner, project, dashboard_uuid, body, (error, data, response) => {
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


## promoteProjectDashboard

> Object promoteProjectDashboard(owner, project, uuid)

Promote project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project
let uuid = "uuid_example"; // String | Uuid identifier of the entity
apiInstance.promoteProjectDashboard(owner, project, uuid, (error, data, response) => {
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
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## updateProjectDashboard

> V1Dashboard updateProjectDashboard(owner, project, dashboard_uuid, body)

Update project dashboard

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectDashboardsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project under namesapce
let dashboard_uuid = "dashboard_uuid_example"; // String | UUID
let body = new PolyaxonSdk.V1Dashboard(); // V1Dashboard | Dashboard body
apiInstance.updateProjectDashboard(owner, project, dashboard_uuid, body, (error, data, response) => {
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


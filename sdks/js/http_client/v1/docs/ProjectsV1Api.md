# PolyaxonSdk.ProjectsV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveProject**](ProjectsV1Api.md#archiveProject) | **POST** /api/v1/{owner}/{name}/archive | Archive project
[**bookmarkProject**](ProjectsV1Api.md#bookmarkProject) | **POST** /api/v1/{owner}/{name}/bookmark | Bookmark project
[**createProject**](ProjectsV1Api.md#createProject) | **POST** /api/v1/{owner}/projects/create | Create new project
[**deleteProject**](ProjectsV1Api.md#deleteProject) | **DELETE** /api/v1/{owner}/{name} | Delete project
[**disableProjectCI**](ProjectsV1Api.md#disableProjectCI) | **DELETE** /api/v1/{owner}/{name}/ci | Disbale project CI
[**enableProjectCI**](ProjectsV1Api.md#enableProjectCI) | **POST** /api/v1/{owner}/{name}/ci | Enable project CI
[**getProject**](ProjectsV1Api.md#getProject) | **GET** /api/v1/{owner}/{name} | Get project
[**getProjectActivities**](ProjectsV1Api.md#getProjectActivities) | **GET** /api/v1/{owner}/{name}/activities | Get project activities
[**getProjectSettings**](ProjectsV1Api.md#getProjectSettings) | **GET** /api/v1/{owner}/{name}/settings | Get Project settings
[**getProjectStats**](ProjectsV1Api.md#getProjectStats) | **GET** /api/v1/{owner}/{name}/stats | Get project stats
[**listArchivedProjects**](ProjectsV1Api.md#listArchivedProjects) | **GET** /api/v1/archives/{user}/projects | List archived projects for user
[**listBookmarkedProjects**](ProjectsV1Api.md#listBookmarkedProjects) | **GET** /api/v1/bookmarks/{user}/projects | List bookmarked projects for user
[**listProjectNames**](ProjectsV1Api.md#listProjectNames) | **GET** /api/v1/{owner}/projects/names | List project names
[**listProjects**](ProjectsV1Api.md#listProjects) | **GET** /api/v1/{owner}/projects/list | List projects
[**patchProject**](ProjectsV1Api.md#patchProject) | **PATCH** /api/v1/{owner}/{project.name} | Patch project
[**patchProjectSettings**](ProjectsV1Api.md#patchProjectSettings) | **PATCH** /api/v1/{owner}/{project}/settings | Patch project settings
[**restoreProject**](ProjectsV1Api.md#restoreProject) | **POST** /api/v1/{owner}/{name}/restore | Restore project
[**unbookmarkProject**](ProjectsV1Api.md#unbookmarkProject) | **DELETE** /api/v1/{owner}/{name}/unbookmark | Unbookmark project
[**updateProject**](ProjectsV1Api.md#updateProject) | **PUT** /api/v1/{owner}/{project.name} | Update project
[**updateProjectSettings**](ProjectsV1Api.md#updateProjectSettings) | **PUT** /api/v1/{owner}/{project}/settings | Update project settings
[**uploadProjectArtifact**](ProjectsV1Api.md#uploadProjectArtifact) | **POST** /api/v1/{owner}/{project}/artifacts/{uuid}/upload | Upload artifact to a store via project access



## archiveProject

> archiveProject(owner, name)

Archive project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.archiveProject(owner, name, (error, data, response) => {
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


## bookmarkProject

> bookmarkProject(owner, name)

Bookmark project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.bookmarkProject(owner, name, (error, data, response) => {
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


## createProject

> V1Project createProject(owner, body)

Create new project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Project(); // V1Project | Project body
apiInstance.createProject(owner, body, (error, data, response) => {
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
 **body** | [**V1Project**](V1Project.md)| Project body | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteProject

> deleteProject(owner, name)

Delete project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.deleteProject(owner, name, (error, data, response) => {
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


## disableProjectCI

> disableProjectCI(owner, name)

Disbale project CI

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.disableProjectCI(owner, name, (error, data, response) => {
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


## enableProjectCI

> enableProjectCI(owner, name)

Enable project CI

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.enableProjectCI(owner, name, (error, data, response) => {
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


## getProject

> V1Project getProject(owner, name)

Get project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getProject(owner, name, (error, data, response) => {
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

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProjectActivities

> V1ListActivitiesResponse getProjectActivities(owner, name, opts)

Get project activities

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.getProjectActivities(owner, name, opts, (error, data, response) => {
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListActivitiesResponse**](V1ListActivitiesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProjectSettings

> V1ProjectSettings getProjectSettings(owner, name)

Get Project settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getProjectSettings(owner, name, (error, data, response) => {
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

[**V1ProjectSettings**](V1ProjectSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProjectStats

> Object getProjectStats(owner, name, opts)

Get project stats

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Entity managing the resource
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'kind': "kind_example", // String | Stats Kind.
  'aggregate': "aggregate_example", // String | Stats aggregate.
  'groupby': "groupby_example", // String | Stats group.
  'trunc': "trunc_example" // String | Stats trunc.
};
apiInstance.getProjectStats(owner, name, opts, (error, data, response) => {
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **kind** | **String**| Stats Kind. | [optional] 
 **aggregate** | **String**| Stats aggregate. | [optional] 
 **groupby** | **String**| Stats group. | [optional] 
 **trunc** | **String**| Stats trunc. | [optional] 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listArchivedProjects

> V1ListProjectsResponse listArchivedProjects(user, opts)

List archived projects for user

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let user = "user_example"; // String | User
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listArchivedProjects(user, opts, (error, data, response) => {
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
 **user** | **String**| User | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listBookmarkedProjects

> V1ListBookmarksResponse listBookmarkedProjects(user, opts)

List bookmarked projects for user

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let user = "user_example"; // String | User
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listBookmarkedProjects(user, opts, (error, data, response) => {
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
 **user** | **String**| User | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListBookmarksResponse**](V1ListBookmarksResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProjectNames

> V1ListProjectsResponse listProjectNames(owner, opts)

List project names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listProjectNames(owner, opts, (error, data, response) => {
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProjects

> V1ListProjectsResponse listProjects(owner, opts)

List projects

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listProjects(owner, opts, (error, data, response) => {
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
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## patchProject

> V1Project patchProject(owner, project_name, body)

Patch project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project_name = "project_name_example"; // String | Required name
let body = new PolyaxonSdk.V1Project(); // V1Project | Project body
apiInstance.patchProject(owner, project_name, body, (error, data, response) => {
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
 **project_name** | **String**| Required name | 
 **body** | [**V1Project**](V1Project.md)| Project body | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchProjectSettings

> V1ProjectSettings patchProjectSettings(owner, project, body)

Patch project settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project name
let body = new PolyaxonSdk.V1ProjectSettings(); // V1ProjectSettings | Project settings body
apiInstance.patchProjectSettings(owner, project, body, (error, data, response) => {
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
 **project** | **String**| Project name | 
 **body** | [**V1ProjectSettings**](V1ProjectSettings.md)| Project settings body | 

### Return type

[**V1ProjectSettings**](V1ProjectSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## restoreProject

> restoreProject(owner, name)

Restore project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.restoreProject(owner, name, (error, data, response) => {
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


## unbookmarkProject

> unbookmarkProject(owner, name)

Unbookmark project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.unbookmarkProject(owner, name, (error, data, response) => {
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


## updateProject

> V1Project updateProject(owner, project_name, body)

Update project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project_name = "project_name_example"; // String | Required name
let body = new PolyaxonSdk.V1Project(); // V1Project | Project body
apiInstance.updateProject(owner, project_name, body, (error, data, response) => {
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
 **project_name** | **String**| Required name | 
 **body** | [**V1Project**](V1Project.md)| Project body | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateProjectSettings

> V1ProjectSettings updateProjectSettings(owner, project, body)

Update project settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project name
let body = new PolyaxonSdk.V1ProjectSettings(); // V1ProjectSettings | Project settings body
apiInstance.updateProjectSettings(owner, project, body, (error, data, response) => {
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
 **project** | **String**| Project name | 
 **body** | [**V1ProjectSettings**](V1ProjectSettings.md)| Project settings body | 

### Return type

[**V1ProjectSettings**](V1ProjectSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## uploadProjectArtifact

> uploadProjectArtifact(owner, project, uuid, uploadfile, opts)

Upload artifact to a store via project access

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.ProjectsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let project = "project_example"; // String | Project having access to the store
let uuid = "uuid_example"; // String | Unique integer identifier of the entity
let uploadfile = "/path/to/file"; // File | The file to upload.
let opts = {
  'path': "path_example", // String | File path query params.
  'overwrite': true // Boolean | File path query params.
};
apiInstance.uploadProjectArtifact(owner, project, uuid, uploadfile, opts, (error, data, response) => {
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
 **project** | **String**| Project having access to the store | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **uploadfile** | **File**| The file to upload. | 
 **path** | **String**| File path query params. | [optional] 
 **overwrite** | **Boolean**| File path query params. | [optional] 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: multipart/form-data
- **Accept**: application/json


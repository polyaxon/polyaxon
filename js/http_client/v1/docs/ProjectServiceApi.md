# PolyaxonSdk.ProjectServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveProject**](ProjectServiceApi.md#archiveProject) | **POST** /api/v1/{owner}/{project}/archive | Stop run
[**bookmarkProject**](ProjectServiceApi.md#bookmarkProject) | **POST** /api/v1/{owner}/{project}/bookmark | Stop run
[**createProject**](ProjectServiceApi.md#createProject) | **POST** /api/v1/{owner}/projects/create | Get run
[**deleteExperiment**](ProjectServiceApi.md#deleteExperiment) | **DELETE** /api/v1/{owner}/projecs/{project} | Delete runs
[**disableProjectCI**](ProjectServiceApi.md#disableProjectCI) | **DELETE** /api/v1/{owner}/{project}/ci | Restart run
[**enableProjectCI**](ProjectServiceApi.md#enableProjectCI) | **POST** /api/v1/{owner}/{project}/ci | Restart run with copy
[**getProject**](ProjectServiceApi.md#getProject) | **GET** /api/v1/{owner}/projects/{project} | Update run
[**listArchivedProjects**](ProjectServiceApi.md#listArchivedProjects) | **GET** /api/v1/archives/{user}/projects | Create new run
[**listBookmarkedProjects**](ProjectServiceApi.md#listBookmarkedProjects) | **GET** /api/v1/bookmarks/{user}/projects | List archived runs for user
[**listProjectNames**](ProjectServiceApi.md#listProjectNames) | **GET** /api/v1/{owner}/projects/names | List bookmarked runs for user
[**listProjects**](ProjectServiceApi.md#listProjects) | **GET** /api/v1/{owner}/projects/list | List runs
[**patchProject**](ProjectServiceApi.md#patchProject) | **PATCH** /api/v1/{owner}/projects/{project} | Delete run
[**restoreExperiment**](ProjectServiceApi.md#restoreExperiment) | **POST** /api/v1/{owner}/{project}/restore | Stop runs
[**unBookmarkProject**](ProjectServiceApi.md#unBookmarkProject) | **DELETE** /api/v1/{owner}/{project}/unbookmark | Invalidate runs
[**updateProject**](ProjectServiceApi.md#updateProject) | **PUT** /api/v1/{owner}/projects/{project} | Patch run


<a name="archiveProject"></a>
# **archiveProject**
> Object archiveProject(owner, project)

Stop run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.archiveProject(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="bookmarkProject"></a>
# **bookmarkProject**
> Object bookmarkProject(owner, project)

Stop run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.bookmarkProject(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createProject"></a>
# **createProject**
> V1Project createProject(owner, body)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var body = new PolyaxonSdk.V1OwnerBodyRequest(); // V1OwnerBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createProject(owner, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OwnerBodyRequest**](V1OwnerBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteExperiment"></a>
# **deleteExperiment**
> Object deleteExperiment(owner, project)

Delete runs

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteExperiment(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="disableProjectCI"></a>
# **disableProjectCI**
> Object disableProjectCI(owner, project)

Restart run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.disableProjectCI(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="enableProjectCI"></a>
# **enableProjectCI**
> Object enableProjectCI(owner, project)

Restart run with copy

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.enableProjectCI(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getProject"></a>
# **getProject**
> V1Project getProject(owner, project)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getProject(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArchivedProjects"></a>
# **listArchivedProjects**
> V1ListProjectsResponse listArchivedProjects(user)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var user = "user_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listArchivedProjects(user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedProjects"></a>
# **listBookmarkedProjects**
> V1ListProjectsResponse listBookmarkedProjects(user)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var user = "user_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listBookmarkedProjects(user, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectNames"></a>
# **listProjectNames**
> V1ListProjectsResponse listProjectNames(owner)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listProjectNames(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjects"></a>
# **listProjects**
> V1ListProjectsResponse listProjects(owner)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.listProjects(owner, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchProject"></a>
# **patchProject**
> V1Project patchProject(owner, project, body)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchProject(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restoreExperiment"></a>
# **restoreExperiment**
> Object restoreExperiment(owner, project)

Stop runs

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restoreExperiment(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="unBookmarkProject"></a>
# **unBookmarkProject**
> Object unBookmarkProject(owner, project)

Invalidate runs

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.unBookmarkProject(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateProject"></a>
# **updateProject**
> V1Project updateProject(owner, project, body)

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

var apiInstance = new PolyaxonSdk.ProjectServiceApi();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1ProjectBodyRequest(); // V1ProjectBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateProject(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1ProjectBodyRequest**](V1ProjectBodyRequest.md)|  | 

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


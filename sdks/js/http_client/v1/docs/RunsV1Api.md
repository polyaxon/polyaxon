# PolyaxonSdk.RunsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveRun**](RunsV1Api.md#archiveRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**bookmarkRun**](RunsV1Api.md#bookmarkRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**copyRun**](RunsV1Api.md#copyRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/copy | Restart run with copy
[**createRun**](RunsV1Api.md#createRun) | **POST** /api/v1/{owner}/{project}/runs/create | Create new run
[**createRunCodeRef**](RunsV1Api.md#createRunCodeRef) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/coderef | Get run code ref
[**createRunStatus**](RunsV1Api.md#createRunStatus) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**deleteRun**](RunsV1Api.md#deleteRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**deleteRuns**](RunsV1Api.md#deleteRuns) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**getRun**](RunsV1Api.md#getRun) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**getRunCodeRefs**](RunsV1Api.md#getRunCodeRefs) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/coderef | Get run code ref
[**getRunStatuses**](RunsV1Api.md#getRunStatuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**impersonateToken**](RunsV1Api.md#impersonateToken) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/impersonate | Impersonate run token
[**invalidateRun**](RunsV1Api.md#invalidateRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Invalidate run
[**invalidateRuns**](RunsV1Api.md#invalidateRuns) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**listArchivedRuns**](RunsV1Api.md#listArchivedRuns) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**listBookmarkedRuns**](RunsV1Api.md#listBookmarkedRuns) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**listRuns**](RunsV1Api.md#listRuns) | **GET** /api/v1/{owner}/{project}/runs/list | List runs
[**patchRun**](RunsV1Api.md#patchRun) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**restartRun**](RunsV1Api.md#restartRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/restart | Restart run
[**restoreRun**](RunsV1Api.md#restoreRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**resumeRun**](RunsV1Api.md#resumeRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/resume | Resume run
[**startRunTensorboard**](RunsV1Api.md#startRunTensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**stopRun**](RunsV1Api.md#stopRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**stopRunTensorboard**](RunsV1Api.md#stopRunTensorboard) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**stopRuns**](RunsV1Api.md#stopRuns) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**unbookmarkRun**](RunsV1Api.md#unbookmarkRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**updateRun**](RunsV1Api.md#updateRun) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run


<a name="archiveRun"></a>
# **archiveRun**
> Object archiveRun(owner, project, uuid)

Archive run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.archiveRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="bookmarkRun"></a>
# **bookmarkRun**
> Object bookmarkRun(owner, project, uuid)

Bookmark run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.bookmarkRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="copyRun"></a>
# **copyRun**
> V1Run copyRun(entity_owner, entity_project, entity_uuid, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_uuid = "entity_uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.copyRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project where the experiement will be assigned | 
 **entity_uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createRun"></a>
# **createRun**
> V1Run createRun(owner, project, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createRun(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createRunCodeRef"></a>
# **createRunCodeRef**
> V1CodeReference createRunCodeRef(entity_owner, entity_project, entity_uuid, body)

Get run code ref

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_uuid = "entity_uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1CodeReference(); // V1CodeReference | Code ref object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createRunCodeRef(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project where the experiement will be assigned | 
 **entity_uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1CodeReference**](V1CodeReference.md)| Code ref object | 

### Return type

[**V1CodeReference**](V1CodeReference.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createRunStatus"></a>
# **createRunStatus**
> V1Status createRunStatus(owner, project, uuid, body)

Create new run status

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1EntityStatusBodyRequest(); // V1EntityStatusBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.createRunStatus(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1EntityStatusBodyRequest**](V1EntityStatusBodyRequest.md)|  | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteRun"></a>
# **deleteRun**
> Object deleteRun(owner, project, uuid)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.deleteRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteRuns"></a>
# **deleteRuns**
> Object deleteRuns(owner, project, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.deleteRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getRun"></a>
# **getRun**
> V1Run getRun(owner, project, uuid)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.getRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getRunCodeRefs"></a>
# **getRunCodeRefs**
> V1ListCodeRefsResponse getRunCodeRefs(owner, project, uuid)

Get run code ref

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.getRunCodeRefs(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1ListCodeRefsResponse**](V1ListCodeRefsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getRunStatuses"></a>
# **getRunStatuses**
> V1Status getRunStatuses(owner, project, uuid)

Get run status

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.getRunStatuses(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="impersonateToken"></a>
# **impersonateToken**
> V1Auth impersonateToken(owner, project, uuid)

Impersonate run token

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.impersonateToken(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="invalidateRun"></a>
# **invalidateRun**
> Object invalidateRun(owner, project, uuid, body)

Invalidate run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.invalidateRun(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="invalidateRuns"></a>
# **invalidateRuns**
> Object invalidateRuns(owner, project, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.invalidateRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArchivedRuns"></a>
# **listArchivedRuns**
> V1ListRunsResponse listArchivedRuns(user, opts)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var user = "user_example"; // String | User

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
apiInstance.listArchivedRuns(user, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedRuns"></a>
# **listBookmarkedRuns**
> V1ListRunsResponse listBookmarkedRuns(user, opts)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var user = "user_example"; // String | User

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
apiInstance.listBookmarkedRuns(user, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listRuns"></a>
# **listRuns**
> V1ListRunsResponse listRuns(owner, project, opts)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.listRuns(owner, project, opts, callback);
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

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchRun"></a>
# **patchRun**
> V1Run patchRun(owner, project, run_uuid, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var run_uuid = "run_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.patchRun(owner, project, run_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **run_uuid** | **String**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restartRun"></a>
# **restartRun**
> V1Run restartRun(entity_owner, entity_project, entity_uuid, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_uuid = "entity_uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.restartRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project where the experiement will be assigned | 
 **entity_uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="restoreRun"></a>
# **restoreRun**
> Object restoreRun(owner, project, uuid)

Restore run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.restoreRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="resumeRun"></a>
# **resumeRun**
> V1Run resumeRun(entity_owner, entity_project, entity_uuid, body)

Resume run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

var entity_owner = "entity_owner_example"; // String | Owner of the namespace

var entity_project = "entity_project_example"; // String | Project where the experiement will be assigned

var entity_uuid = "entity_uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.resumeRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project where the experiement will be assigned | 
 **entity_uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="startRunTensorboard"></a>
# **startRunTensorboard**
> Object startRunTensorboard(owner, project, uuid, body)

Start run tensorboard

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var body = new PolyaxonSdk.V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.startRunTensorboard(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopRun"></a>
# **stopRun**
> Object stopRun(owner, project, uuid)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.stopRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopRunTensorboard"></a>
# **stopRunTensorboard**
> Object stopRunTensorboard(owner, project, uuid)

Stop run tensorboard

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.stopRunTensorboard(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="stopRuns"></a>
# **stopRuns**
> Object stopRuns(owner, project, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project under namesapce

var body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.stopRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="unbookmarkRun"></a>
# **unbookmarkRun**
> Object unbookmarkRun(owner, project, uuid)

Unbookmark run

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.RunsV1Api();

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
apiInstance.unbookmarkRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateRun"></a>
# **updateRun**
> V1Run updateRun(owner, project, run_uuid, body)

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

var apiInstance = new PolyaxonSdk.RunsV1Api();

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var run_uuid = "run_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.updateRun(owner, project, run_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **run_uuid** | **String**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


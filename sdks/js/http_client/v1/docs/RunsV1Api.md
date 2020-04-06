# PolyaxonSdk.RunsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getRunArtifact**](RunsV1Api.md#getRunArtifact) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifact | Get run artifact
[**getRunArtifacts**](RunsV1Api.md#getRunArtifacts) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts | Get run artifacts
[**runsV1ArchiveRun**](RunsV1Api.md#runsV1ArchiveRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**runsV1BookmarkRun**](RunsV1Api.md#runsV1BookmarkRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**runsV1BookmarkRuns**](RunsV1Api.md#runsV1BookmarkRuns) | **POST** /api/v1/{owner}/{project}/runs/bookmark | Bookmark runs
[**runsV1CollectRunLogs**](RunsV1Api.md#runsV1CollectRunLogs) | **POST** /streams/v1/{namespace}/_internal/{owner}/{project}/runs/{uuid}/logs | Collect run logs
[**runsV1CopyRun**](RunsV1Api.md#runsV1CopyRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/copy | Restart run with copy
[**runsV1CreateRun**](RunsV1Api.md#runsV1CreateRun) | **POST** /api/v1/{owner}/{project}/runs | Create new run
[**runsV1CreateRunArtifactsLineage**](RunsV1Api.md#runsV1CreateRunArtifactsLineage) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Create bulk run run artifacts lineage
[**runsV1CreateRunStatus**](RunsV1Api.md#runsV1CreateRunStatus) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**runsV1DeleteRun**](RunsV1Api.md#runsV1DeleteRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**runsV1DeleteRunArtifactLineage**](RunsV1Api.md#runsV1DeleteRunArtifactLineage) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Delete run artifact lineage
[**runsV1DeleteRuns**](RunsV1Api.md#runsV1DeleteRuns) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**runsV1GetMultiRunEvents**](RunsV1Api.md#runsV1GetMultiRunEvents) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/multi/events/{kind} | Get multi runs events
[**runsV1GetRun**](RunsV1Api.md#runsV1GetRun) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**runsV1GetRunArtifactLineage**](RunsV1Api.md#runsV1GetRunArtifactLineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Get run artifacts lineage
[**runsV1GetRunArtifactsLineage**](RunsV1Api.md#runsV1GetRunArtifactsLineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Get run artifacts lineage
[**runsV1GetRunArtifactsLineageNames**](RunsV1Api.md#runsV1GetRunArtifactsLineageNames) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/names | Get run artifacts lineage names
[**runsV1GetRunArtifactsTree**](RunsV1Api.md#runsV1GetRunArtifactsTree) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts/tree | Get run artifacts tree
[**runsV1GetRunEvents**](RunsV1Api.md#runsV1GetRunEvents) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/events/{kind} | Get run events
[**runsV1GetRunLogs**](RunsV1Api.md#runsV1GetRunLogs) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/logs | Get run logs
[**runsV1GetRunNamespace**](RunsV1Api.md#runsV1GetRunNamespace) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/namespace | Get Run namespace
[**runsV1GetRunResources**](RunsV1Api.md#runsV1GetRunResources) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/resources | Get run resources events
[**runsV1GetRunSettings**](RunsV1Api.md#runsV1GetRunSettings) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/settings | Get Run settings
[**runsV1GetRunStatuses**](RunsV1Api.md#runsV1GetRunStatuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**runsV1GetRunsArtifactsLineage**](RunsV1Api.md#runsV1GetRunsArtifactsLineage) | **GET** /api/v1/{owner}/{project}/runs/artifacts_lineage | Get runs artifacts lineage
[**runsV1ImpersonateToken**](RunsV1Api.md#runsV1ImpersonateToken) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/impersonate | Impersonate run token
[**runsV1InvalidateRun**](RunsV1Api.md#runsV1InvalidateRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Invalidate run
[**runsV1InvalidateRuns**](RunsV1Api.md#runsV1InvalidateRuns) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**runsV1ListArchivedRuns**](RunsV1Api.md#runsV1ListArchivedRuns) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**runsV1ListBookmarkedRuns**](RunsV1Api.md#runsV1ListBookmarkedRuns) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**runsV1ListRuns**](RunsV1Api.md#runsV1ListRuns) | **GET** /api/v1/{owner}/{project}/runs | List runs
[**runsV1ListRunsIo**](RunsV1Api.md#runsV1ListRunsIo) | **GET** /api/v1/{owner}/{project}/runs/io | List runs io
[**runsV1NotifyRunStatus**](RunsV1Api.md#runsV1NotifyRunStatus) | **POST** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/notify | Notify run status
[**runsV1PatchRun**](RunsV1Api.md#runsV1PatchRun) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**runsV1RestartRun**](RunsV1Api.md#runsV1RestartRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/restart | Restart run
[**runsV1RestoreRun**](RunsV1Api.md#runsV1RestoreRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**runsV1ResumeRun**](RunsV1Api.md#runsV1ResumeRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/resume | Resume run
[**runsV1StartRunTensorboard**](RunsV1Api.md#runsV1StartRunTensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**runsV1StopRun**](RunsV1Api.md#runsV1StopRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**runsV1StopRunTensorboard**](RunsV1Api.md#runsV1StopRunTensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**runsV1StopRuns**](RunsV1Api.md#runsV1StopRuns) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**runsV1TagRuns**](RunsV1Api.md#runsV1TagRuns) | **POST** /api/v1/{owner}/{project}/runs/tag | Tag runs
[**runsV1UnbookmarkRun**](RunsV1Api.md#runsV1UnbookmarkRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**runsV1UpdateRun**](RunsV1Api.md#runsV1UpdateRun) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run
[**uploadRunArtifact**](RunsV1Api.md#uploadRunArtifact) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts/upload | Upload an artifact file to a store via run access
[**uploadRunLogs**](RunsV1Api.md#uploadRunLogs) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/logs/upload | Upload a logs file to a store via run access


<a name="getRunArtifact"></a>
# **getRunArtifact**
> 'String' getRunArtifact(namespace, owner, project, uuid, opts)

Get run artifact

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var opts = { 
  'path': "path_example", // String | Artifact filepath.
  'stream': true // Boolean | Whether to stream the file.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getRunArtifact(namespace, owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **path** | **String**| Artifact filepath. | [optional] 
 **stream** | **Boolean**| Whether to stream the file. | [optional] 

### Return type

**'String'**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getRunArtifacts"></a>
# **getRunArtifacts**
> 'String' getRunArtifacts(namespace, owner, project, uuid, opts)

Get run artifacts

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the experiement will be assigned

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var opts = { 
  'path': "path_example" // String | Artifact filepath.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getRunArtifacts(namespace, owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the experiement will be assigned | 
 **uuid** | **String**| Unique integer identifier of the entity | 
 **path** | **String**| Artifact filepath. | [optional] 

### Return type

**'String'**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1ArchiveRun"></a>
# **runsV1ArchiveRun**
> runsV1ArchiveRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1ArchiveRun(owner, project, uuid, callback);
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

<a name="runsV1BookmarkRun"></a>
# **runsV1BookmarkRun**
> runsV1BookmarkRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1BookmarkRun(owner, project, uuid, callback);
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

<a name="runsV1BookmarkRuns"></a>
# **runsV1BookmarkRuns**
> runsV1BookmarkRuns(owner, project, body)

Bookmark runs

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
    console.log('API called successfully.');
  }
};
apiInstance.runsV1BookmarkRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1CollectRunLogs"></a>
# **runsV1CollectRunLogs**
> runsV1CollectRunLogs(namespace, owner, project, uuid)

Collect run logs

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

var namespace = "namespace_example"; // String | 

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1CollectRunLogs(namespace, owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**|  | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1CopyRun"></a>
# **runsV1CopyRun**
> V1Run runsV1CopyRun(entity_owner, entity_project, entity_uuid, body)

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

var entity_project = "entity_project_example"; // String | Project

var entity_uuid = "entity_uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1CopyRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project | 
 **entity_uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1CreateRun"></a>
# **runsV1CreateRun**
> V1Run runsV1CreateRun(owner, project, body)

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

var project = "project_example"; // String | Project where the run will be assigned

var body = new PolyaxonSdk.V1OperationBody(); // V1OperationBody | operation object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1CreateRun(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **body** | [**V1OperationBody**](V1OperationBody.md)| operation object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1CreateRunArtifactsLineage"></a>
# **runsV1CreateRunArtifactsLineage**
> runsV1CreateRunArtifactsLineage(owner, project, uuid, body)

Create bulk run run artifacts lineage

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1RunArtifacts(); // V1RunArtifacts | Run Artifacts


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1CreateRunArtifactsLineage(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1RunArtifacts**](V1RunArtifacts.md)| Run Artifacts | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1CreateRunStatus"></a>
# **runsV1CreateRunStatus**
> V1Status runsV1CreateRunStatus(owner, project, uuid, body)

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1EntityStatusBodyRequest(); // V1EntityStatusBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1CreateRunStatus(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1EntityStatusBodyRequest**](V1EntityStatusBodyRequest.md)|  | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1DeleteRun"></a>
# **runsV1DeleteRun**
> runsV1DeleteRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1DeleteRun(owner, project, uuid, callback);
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

<a name="runsV1DeleteRunArtifactLineage"></a>
# **runsV1DeleteRunArtifactLineage**
> runsV1DeleteRunArtifactLineage(owner, project, uuid, name, opts)

Delete run artifact lineage

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var name = "name_example"; // String | Artifact name

var opts = { 
  'namespace': "namespace_example" // String | namespace.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1DeleteRunArtifactLineage(owner, project, uuid, name, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **name** | **String**| Artifact name | 
 **namespace** | **String**| namespace. | [optional] 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1DeleteRuns"></a>
# **runsV1DeleteRuns**
> runsV1DeleteRuns(owner, project, body)

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
    console.log('API called successfully.');
  }
};
apiInstance.runsV1DeleteRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetMultiRunEvents"></a>
# **runsV1GetMultiRunEvents**
> V1EventsResponse runsV1GetMultiRunEvents(namespace, owner, project, kind, opts)

Get multi runs events

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var kind = "kind_example"; // String | The artifact kind

var opts = { 
  'names': "names_example", // String | Names query param.
  'runs': "runs_example", // String | Runs query param.
  'orient': "orient_example" // String | Orient query param.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetMultiRunEvents(namespace, owner, project, kind, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **kind** | **String**| The artifact kind | 
 **names** | **String**| Names query param. | [optional] 
 **runs** | **String**| Runs query param. | [optional] 
 **orient** | **String**| Orient query param. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRun"></a>
# **runsV1GetRun**
> V1Run runsV1GetRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRun(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunArtifactLineage"></a>
# **runsV1GetRunArtifactLineage**
> V1RunArtifact runsV1GetRunArtifactLineage(owner, project, uuid, name, opts)

Get run artifacts lineage

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var name = "name_example"; // String | Artifact name

var opts = { 
  'namespace': "namespace_example" // String | namespace.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunArtifactLineage(owner, project, uuid, name, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **name** | **String**| Artifact name | 
 **namespace** | **String**| namespace. | [optional] 

### Return type

[**V1RunArtifact**](V1RunArtifact.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunArtifactsLineage"></a>
# **runsV1GetRunArtifactsLineage**
> V1ListRunArtifactsResponse runsV1GetRunArtifactsLineage(owner, project, uuid, opts)

Get run artifacts lineage

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var opts = { 
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
apiInstance.runsV1GetRunArtifactsLineage(owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunArtifactsLineageNames"></a>
# **runsV1GetRunArtifactsLineageNames**
> V1ListRunArtifactsResponse runsV1GetRunArtifactsLineageNames(owner, project, uuid, opts)

Get run artifacts lineage names

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

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var opts = { 
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
apiInstance.runsV1GetRunArtifactsLineageNames(owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search search. | [optional] 

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunArtifactsTree"></a>
# **runsV1GetRunArtifactsTree**
> V1ArtifactTree runsV1GetRunArtifactsTree(namespace, owner, project, uuid, opts)

Get run artifacts tree

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var opts = { 
  'path': "path_example" // String | Path query param.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunArtifactsTree(namespace, owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **path** | **String**| Path query param. | [optional] 

### Return type

[**V1ArtifactTree**](V1ArtifactTree.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunEvents"></a>
# **runsV1GetRunEvents**
> V1EventsResponse runsV1GetRunEvents(namespace, owner, project, uuid, kind, opts)

Get run events

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var kind = "kind_example"; // String | The artifact kind

var opts = { 
  'names': "names_example", // String | Names query param.
  'orient': "orient_example" // String | Orient query param.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunEvents(namespace, owner, project, uuid, kind, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **kind** | **String**| The artifact kind | 
 **names** | **String**| Names query param. | [optional] 
 **orient** | **String**| Orient query param. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunLogs"></a>
# **runsV1GetRunLogs**
> V1Logs runsV1GetRunLogs(namespace, owner, project, uuid, opts)

Get run logs

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

var namespace = "namespace_example"; // String | 

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var opts = { 
  'last_time': new Date("2013-10-20T19:20:30+01:00"), // Date | last time.
  'last_file': "last_file_example" // String | last file.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunLogs(namespace, owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**|  | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **last_time** | **Date**| last time. | [optional] 
 **last_file** | **String**| last file. | [optional] 

### Return type

[**V1Logs**](V1Logs.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunNamespace"></a>
# **runsV1GetRunNamespace**
> V1RunSettings runsV1GetRunNamespace(owner, project, uuid)

Get Run namespace

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunNamespace(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1RunSettings**](V1RunSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunResources"></a>
# **runsV1GetRunResources**
> V1EventsResponse runsV1GetRunResources(namespace, owner, project, uuid, opts)

Get run resources events

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

var namespace = "namespace_example"; // String | namespace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var opts = { 
  'names': "names_example", // String | Names query param.
  'tail': true // Boolean | Query param flag to tail the values.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunResources(namespace, owner, project, uuid, opts, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **names** | **String**| Names query param. | [optional] 
 **tail** | **Boolean**| Query param flag to tail the values. | [optional] 

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunSettings"></a>
# **runsV1GetRunSettings**
> V1RunSettings runsV1GetRunSettings(owner, project, uuid)

Get Run settings

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunSettings(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1RunSettings**](V1RunSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunStatuses"></a>
# **runsV1GetRunStatuses**
> V1Status runsV1GetRunStatuses(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1GetRunStatuses(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Status**](V1Status.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1GetRunsArtifactsLineage"></a>
# **runsV1GetRunsArtifactsLineage**
> runsV1GetRunsArtifactsLineage(owner, project)

Get runs artifacts lineage

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


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1GetRunsArtifactsLineage(owner, project, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1ImpersonateToken"></a>
# **runsV1ImpersonateToken**
> V1Auth runsV1ImpersonateToken(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1ImpersonateToken(owner, project, uuid, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1InvalidateRun"></a>
# **runsV1InvalidateRun**
> runsV1InvalidateRun(owner, project, uuid, body)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1InvalidateRun(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1InvalidateRuns"></a>
# **runsV1InvalidateRuns**
> runsV1InvalidateRuns(owner, project, body)

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
    console.log('API called successfully.');
  }
};
apiInstance.runsV1InvalidateRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1ListArchivedRuns"></a>
# **runsV1ListArchivedRuns**
> V1ListRunsResponse runsV1ListArchivedRuns(user, opts)

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
apiInstance.runsV1ListArchivedRuns(user, opts, callback);
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

<a name="runsV1ListBookmarkedRuns"></a>
# **runsV1ListBookmarkedRuns**
> V1ListRunsResponse runsV1ListBookmarkedRuns(user, opts)

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
apiInstance.runsV1ListBookmarkedRuns(user, opts, callback);
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

<a name="runsV1ListRuns"></a>
# **runsV1ListRuns**
> V1ListRunsResponse runsV1ListRuns(owner, project, opts)

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
apiInstance.runsV1ListRuns(owner, project, opts, callback);
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

<a name="runsV1ListRunsIo"></a>
# **runsV1ListRunsIo**
> V1ListRunsResponse runsV1ListRunsIo(owner, project, opts)

List runs io

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
apiInstance.runsV1ListRunsIo(owner, project, opts, callback);
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

<a name="runsV1NotifyRunStatus"></a>
# **runsV1NotifyRunStatus**
> runsV1NotifyRunStatus(namespace, owner, project, uuid, body)

Notify run status

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

var namespace = "namespace_example"; // String | Na,espace

var owner = "owner_example"; // String | Owner of the namespace

var project = "project_example"; // String | Project where the run will be assigned

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1EntityNotificationBody(); // V1EntityNotificationBody | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1NotifyRunStatus(namespace, owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| Na,espace | 
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1EntityNotificationBody**](V1EntityNotificationBody.md)|  | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1PatchRun"></a>
# **runsV1PatchRun**
> V1Run runsV1PatchRun(owner, project, run_uuid, body)

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

var project = "project_example"; // String | Project where the run will be assigned

var run_uuid = "run_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1PatchRun(owner, project, run_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **run_uuid** | **String**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1RestartRun"></a>
# **runsV1RestartRun**
> V1Run runsV1RestartRun(entity_owner, entity_project, entity_uuid, body)

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

var entity_project = "entity_project_example"; // String | Project

var entity_uuid = "entity_uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1RestartRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project | 
 **entity_uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1RestoreRun"></a>
# **runsV1RestoreRun**
> runsV1RestoreRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1RestoreRun(owner, project, uuid, callback);
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

<a name="runsV1ResumeRun"></a>
# **runsV1ResumeRun**
> V1Run runsV1ResumeRun(entity_owner, entity_project, entity_uuid, body)

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

var entity_project = "entity_project_example"; // String | Project

var entity_uuid = "entity_uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1ResumeRun(entity_owner, entity_project, entity_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_owner** | **String**| Owner of the namespace | 
 **entity_project** | **String**| Project | 
 **entity_uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1StartRunTensorboard"></a>
# **runsV1StartRunTensorboard**
> runsV1StartRunTensorboard(owner, project, uuid, body)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity

var body = new PolyaxonSdk.V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1StartRunTensorboard(owner, project, uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project | 
 **uuid** | **String**| Uuid identifier of the entity | 
 **body** | [**V1ProjectEntityResourceRequest**](V1ProjectEntityResourceRequest.md)|  | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1StopRun"></a>
# **runsV1StopRun**
> runsV1StopRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1StopRun(owner, project, uuid, callback);
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

<a name="runsV1StopRunTensorboard"></a>
# **runsV1StopRunTensorboard**
> runsV1StopRunTensorboard(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1StopRunTensorboard(owner, project, uuid, callback);
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

<a name="runsV1StopRuns"></a>
# **runsV1StopRuns**
> runsV1StopRuns(owner, project, body)

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
    console.log('API called successfully.');
  }
};
apiInstance.runsV1StopRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1TagRuns"></a>
# **runsV1TagRuns**
> runsV1TagRuns(owner, project, body)

Tag runs

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
    console.log('API called successfully.');
  }
};
apiInstance.runsV1TagRuns(owner, project, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project under namesapce | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runsV1UnbookmarkRun"></a>
# **runsV1UnbookmarkRun**
> runsV1UnbookmarkRun(owner, project, uuid)

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

var project = "project_example"; // String | Project

var uuid = "uuid_example"; // String | Uuid identifier of the entity


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.runsV1UnbookmarkRun(owner, project, uuid, callback);
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

<a name="runsV1UpdateRun"></a>
# **runsV1UpdateRun**
> V1Run runsV1UpdateRun(owner, project, run_uuid, body)

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

var project = "project_example"; // String | Project where the run will be assigned

var run_uuid = "run_uuid_example"; // String | UUID

var body = new PolyaxonSdk.V1Run(); // V1Run | Run object


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.runsV1UpdateRun(owner, project, run_uuid, body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **project** | **String**| Project where the run will be assigned | 
 **run_uuid** | **String**| UUID | 
 **body** | [**V1Run**](V1Run.md)| Run object | 

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="uploadRunArtifact"></a>
# **uploadRunArtifact**
> uploadRunArtifact(owner, project, uuid, uploadfile, opts)

Upload an artifact file to a store via run access

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

var project = "project_example"; // String | Project having access to the store

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var uploadfile = "/path/to/file.txt"; // File | The file to upload.

var opts = { 
  'path': "path_example", // String | File path query params.
  'overwrite': true // Boolean | File path query params.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.uploadRunArtifact(owner, project, uuid, uploadfile, opts, callback);
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

<a name="uploadRunLogs"></a>
# **uploadRunLogs**
> uploadRunLogs(owner, project, uuid, uploadfile, opts)

Upload a logs file to a store via run access

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

var project = "project_example"; // String | Project having access to the store

var uuid = "uuid_example"; // String | Unique integer identifier of the entity

var uploadfile = "/path/to/file.txt"; // File | The file to upload.

var opts = { 
  'path': "path_example", // String | File path query params.
  'overwrite': true // Boolean | File path query params.
};

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.uploadRunLogs(owner, project, uuid, uploadfile, opts, callback);
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


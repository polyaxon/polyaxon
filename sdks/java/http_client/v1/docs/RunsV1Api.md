# RunsV1Api

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
> String getRunArtifact(namespace, owner, project, uuid, path, stream)

Get run artifact

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
String path = "path_example"; // String | Artifact filepath.
Boolean stream = true; // Boolean | Whether to stream the file.
try {
    String result = apiInstance.getRunArtifact(namespace, owner, project, uuid, path, stream);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#getRunArtifact");
    e.printStackTrace();
}
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

**String**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getRunArtifacts"></a>
# **getRunArtifacts**
> String getRunArtifacts(namespace, owner, project, uuid, path)

Get run artifacts

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
String path = "path_example"; // String | Artifact filepath.
try {
    String result = apiInstance.getRunArtifacts(namespace, owner, project, uuid, path);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#getRunArtifacts");
    e.printStackTrace();
}
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

**String**

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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1ArchiveRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ArchiveRun");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1BookmarkRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1BookmarkRun");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
try {
    apiInstance.runsV1BookmarkRuns(owner, project, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1BookmarkRuns");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | 
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1CollectRunLogs(namespace, owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1CollectRunLogs");
    e.printStackTrace();
}
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
> V1Run runsV1CopyRun(entityOwner, entityProject, entityUuid, body)

Restart run with copy

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String entityOwner = "entityOwner_example"; // String | Owner of the namespace
String entityProject = "entityProject_example"; // String | Project
String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.runsV1CopyRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1CopyRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project |
 **entityUuid** | **String**| Uuid identifier of the entity |
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
V1OperationBody body = new V1OperationBody(); // V1OperationBody | operation object
try {
    V1Run result = apiInstance.runsV1CreateRun(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1CreateRun");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1RunArtifacts body = new V1RunArtifacts(); // V1RunArtifacts | Run Artifacts
try {
    apiInstance.runsV1CreateRunArtifactsLineage(owner, project, uuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1CreateRunArtifactsLineage");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1EntityStatusBodyRequest body = new V1EntityStatusBodyRequest(); // V1EntityStatusBodyRequest | 
try {
    V1Status result = apiInstance.runsV1CreateRunStatus(owner, project, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1CreateRunStatus");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1DeleteRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1DeleteRun");
    e.printStackTrace();
}
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
> runsV1DeleteRunArtifactLineage(owner, project, uuid, name, namespace)

Delete run artifact lineage

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
String name = "name_example"; // String | Artifact name
String namespace = "namespace_example"; // String | namespace.
try {
    apiInstance.runsV1DeleteRunArtifactLineage(owner, project, uuid, name, namespace);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1DeleteRunArtifactLineage");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
try {
    apiInstance.runsV1DeleteRuns(owner, project, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1DeleteRuns");
    e.printStackTrace();
}
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
> V1EventsResponse runsV1GetMultiRunEvents(namespace, owner, project, kind, names, runs, orient)

Get multi runs events

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String kind = "kind_example"; // String | The artifact kind
String names = "names_example"; // String | Names query param.
String runs = "runs_example"; // String | Runs query param.
String orient = "orient_example"; // String | Orient query param.
try {
    V1EventsResponse result = apiInstance.runsV1GetMultiRunEvents(namespace, owner, project, kind, names, runs, orient);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetMultiRunEvents");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace |
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **kind** | **String**| The artifact kind | [enum: model, audio, video, histogram, image, tensor, dataframe, chart, csv, tsv, psv, ssv, metric, env, html, text, file, dir, dockerfile, docker_image, data, coderef, table]
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Run result = apiInstance.runsV1GetRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRun");
    e.printStackTrace();
}
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
> V1RunArtifact runsV1GetRunArtifactLineage(owner, project, uuid, name, namespace)

Get run artifacts lineage

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
String name = "name_example"; // String | Artifact name
String namespace = "namespace_example"; // String | namespace.
try {
    V1RunArtifact result = apiInstance.runsV1GetRunArtifactLineage(owner, project, uuid, name, namespace);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunArtifactLineage");
    e.printStackTrace();
}
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
> V1ListRunArtifactsResponse runsV1GetRunArtifactsLineage(owner, project, uuid, limit, sort, query)

Get run artifacts lineage

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunArtifactsResponse result = apiInstance.runsV1GetRunArtifactsLineage(owner, project, uuid, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunArtifactsLineage");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **uuid** | **String**| Uuid identifier of the entity |
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListRunArtifactsResponse runsV1GetRunArtifactsLineageNames(owner, project, uuid, limit, sort, query)

Get run artifacts lineage names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunArtifactsResponse result = apiInstance.runsV1GetRunArtifactsLineageNames(owner, project, uuid, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunArtifactsLineageNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **uuid** | **String**| Uuid identifier of the entity |
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ArtifactTree runsV1GetRunArtifactsTree(namespace, owner, project, uuid, path)

Get run artifacts tree

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
String path = "path_example"; // String | Path query param.
try {
    V1ArtifactTree result = apiInstance.runsV1GetRunArtifactsTree(namespace, owner, project, uuid, path);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunArtifactsTree");
    e.printStackTrace();
}
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
> V1EventsResponse runsV1GetRunEvents(namespace, owner, project, uuid, kind, names, orient)

Get run events

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
String kind = "kind_example"; // String | The artifact kind
String names = "names_example"; // String | Names query param.
String orient = "orient_example"; // String | Orient query param.
try {
    V1EventsResponse result = apiInstance.runsV1GetRunEvents(namespace, owner, project, uuid, kind, names, orient);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunEvents");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace |
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **uuid** | **String**| Uuid identifier of the entity |
 **kind** | **String**| The artifact kind | [enum: model, audio, video, histogram, image, tensor, dataframe, chart, csv, tsv, psv, ssv, metric, env, html, text, file, dir, dockerfile, docker_image, data, coderef, table]
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
> V1Logs runsV1GetRunLogs(namespace, owner, project, uuid, lastTime, lastFile)

Get run logs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | 
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
OffsetDateTime lastTime = OffsetDateTime.now(); // OffsetDateTime | last time.
String lastFile = "lastFile_example"; // String | last file.
try {
    V1Logs result = apiInstance.runsV1GetRunLogs(namespace, owner, project, uuid, lastTime, lastFile);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunLogs");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**|  |
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **uuid** | **String**| Uuid identifier of the entity |
 **lastTime** | **OffsetDateTime**| last time. | [optional]
 **lastFile** | **String**| last file. | [optional]

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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1RunSettings result = apiInstance.runsV1GetRunNamespace(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunNamespace");
    e.printStackTrace();
}
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
> V1EventsResponse runsV1GetRunResources(namespace, owner, project, uuid, names, tail)

Get run resources events

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | namespace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
String names = "names_example"; // String | Names query param.
Boolean tail = true; // Boolean | Query param flag to tail the values.
try {
    V1EventsResponse result = apiInstance.runsV1GetRunResources(namespace, owner, project, uuid, names, tail);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunResources");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1RunSettings result = apiInstance.runsV1GetRunSettings(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunSettings");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Status result = apiInstance.runsV1GetRunStatuses(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunStatuses");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    apiInstance.runsV1GetRunsArtifactsLineage(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1GetRunsArtifactsLineage");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Auth result = apiInstance.runsV1ImpersonateToken(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ImpersonateToken");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1ProjectEntityResourceRequest body = new V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 
try {
    apiInstance.runsV1InvalidateRun(owner, project, uuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1InvalidateRun");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
try {
    apiInstance.runsV1InvalidateRuns(owner, project, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1InvalidateRuns");
    e.printStackTrace();
}
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
> V1ListRunsResponse runsV1ListArchivedRuns(user, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String user = "user_example"; // String | User
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunsResponse result = apiInstance.runsV1ListArchivedRuns(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ListArchivedRuns");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListRunsResponse runsV1ListBookmarkedRuns(user, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String user = "user_example"; // String | User
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunsResponse result = apiInstance.runsV1ListBookmarkedRuns(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ListBookmarkedRuns");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListRunsResponse runsV1ListRuns(owner, project, offset, limit, sort, query)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunsResponse result = apiInstance.runsV1ListRuns(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ListRuns");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
> V1ListRunsResponse runsV1ListRunsIo(owner, project, offset, limit, sort, query)

List runs io

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunsResponse result = apiInstance.runsV1ListRunsIo(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ListRunsIo");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String namespace = "namespace_example"; // String | Na,espace
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1EntityNotificationBody body = new V1EntityNotificationBody(); // V1EntityNotificationBody | 
try {
    apiInstance.runsV1NotifyRunStatus(namespace, owner, project, uuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1NotifyRunStatus");
    e.printStackTrace();
}
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
> V1Run runsV1PatchRun(owner, project, runUuid, body)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String runUuid = "runUuid_example"; // String | UUID
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.runsV1PatchRun(owner, project, runUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1PatchRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **runUuid** | **String**| UUID |
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
> V1Run runsV1RestartRun(entityOwner, entityProject, entityUuid, body)

Restart run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String entityOwner = "entityOwner_example"; // String | Owner of the namespace
String entityProject = "entityProject_example"; // String | Project
String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.runsV1RestartRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1RestartRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project |
 **entityUuid** | **String**| Uuid identifier of the entity |
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1RestoreRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1RestoreRun");
    e.printStackTrace();
}
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
> V1Run runsV1ResumeRun(entityOwner, entityProject, entityUuid, body)

Resume run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String entityOwner = "entityOwner_example"; // String | Owner of the namespace
String entityProject = "entityProject_example"; // String | Project
String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.runsV1ResumeRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1ResumeRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project |
 **entityUuid** | **String**| Uuid identifier of the entity |
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
V1ProjectEntityResourceRequest body = new V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 
try {
    apiInstance.runsV1StartRunTensorboard(owner, project, uuid, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1StartRunTensorboard");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1StopRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1StopRun");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1StopRunTensorboard(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1StopRunTensorboard");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
try {
    apiInstance.runsV1StopRuns(owner, project, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1StopRuns");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
try {
    apiInstance.runsV1TagRuns(owner, project, body);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1TagRuns");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runsV1UnbookmarkRun(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1UnbookmarkRun");
    e.printStackTrace();
}
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
> V1Run runsV1UpdateRun(owner, project, runUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the run will be assigned
String runUuid = "runUuid_example"; // String | UUID
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.runsV1UpdateRun(owner, project, runUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#runsV1UpdateRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **runUuid** | **String**| UUID |
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
> uploadRunArtifact(owner, project, uuid, uploadfile, path, overwrite)

Upload an artifact file to a store via run access

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project having access to the store
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
File uploadfile = new File("/path/to/file.txt"); // File | The file to upload.
String path = "path_example"; // String | File path query params.
Boolean overwrite = true; // Boolean | File path query params.
try {
    apiInstance.uploadRunArtifact(owner, project, uuid, uploadfile, path, overwrite);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#uploadRunArtifact");
    e.printStackTrace();
}
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
> uploadRunLogs(owner, project, uuid, uploadfile, path, overwrite)

Upload a logs file to a store via run access

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunsV1Api apiInstance = new RunsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project having access to the store
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
File uploadfile = new File("/path/to/file.txt"); // File | The file to upload.
String path = "path_example"; // String | File path query params.
Boolean overwrite = true; // Boolean | File path query params.
try {
    apiInstance.uploadRunLogs(owner, project, uuid, uploadfile, path, overwrite);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#uploadRunLogs");
    e.printStackTrace();
}
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


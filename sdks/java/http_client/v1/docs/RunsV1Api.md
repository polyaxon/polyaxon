# RunsV1Api
Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveRun**](RunsV1Api.md#archiveRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/archive | Archive run
[**bookmarkRun**](RunsV1Api.md#bookmarkRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/bookmark | Bookmark run
[**bookmarkRuns**](RunsV1Api.md#bookmarkRuns) | **POST** /api/v1/{owner}/{project}/runs/bookmark | Bookmark runs
[**collectRunLogs**](RunsV1Api.md#collectRunLogs) | **POST** /streams/v1/{namespace}/_internal/{owner}/{project}/runs/{uuid}/logs | Collect run logs
[**copyRun**](RunsV1Api.md#copyRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/copy | Restart run with copy
[**createRun**](RunsV1Api.md#createRun) | **POST** /api/v1/{owner}/{project}/runs | Create new run
[**createRunArtifactsLineage**](RunsV1Api.md#createRunArtifactsLineage) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Create bulk run run artifacts lineage
[**createRunStatus**](RunsV1Api.md#createRunStatus) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Create new run status
[**deleteRun**](RunsV1Api.md#deleteRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid} | Delete run
[**deleteRunArtifactLineage**](RunsV1Api.md#deleteRunArtifactLineage) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Delete run artifact lineage
[**deleteRuns**](RunsV1Api.md#deleteRuns) | **DELETE** /api/v1/{owner}/{project}/runs/delete | Delete runs
[**getMultiRunEvents**](RunsV1Api.md#getMultiRunEvents) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/multi/events/{kind} | Get multi runs events
[**getRun**](RunsV1Api.md#getRun) | **GET** /api/v1/{owner}/{project}/runs/{uuid} | Get run
[**getRunArtifact**](RunsV1Api.md#getRunArtifact) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifact | Get run artifact
[**getRunArtifactLineage**](RunsV1Api.md#getRunArtifactLineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/{name} | Get run artifacts lineage
[**getRunArtifacts**](RunsV1Api.md#getRunArtifacts) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts | Get run artifacts
[**getRunArtifactsLineage**](RunsV1Api.md#getRunArtifactsLineage) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage | Get run artifacts lineage
[**getRunArtifactsLineageNames**](RunsV1Api.md#getRunArtifactsLineageNames) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/artifacts_lineage/names | Get run artifacts lineage names
[**getRunArtifactsTree**](RunsV1Api.md#getRunArtifactsTree) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/artifacts/tree | Get run artifacts tree
[**getRunEvents**](RunsV1Api.md#getRunEvents) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/events/{kind} | Get run events
[**getRunLogs**](RunsV1Api.md#getRunLogs) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/logs | Get run logs
[**getRunNamespace**](RunsV1Api.md#getRunNamespace) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/namespace | Get Run namespace
[**getRunResources**](RunsV1Api.md#getRunResources) | **GET** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/resources | Get run resources events
[**getRunSettings**](RunsV1Api.md#getRunSettings) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/settings | Get Run settings
[**getRunStatuses**](RunsV1Api.md#getRunStatuses) | **GET** /api/v1/{owner}/{project}/runs/{uuid}/statuses | Get run status
[**getRunsArtifactsLineage**](RunsV1Api.md#getRunsArtifactsLineage) | **GET** /api/v1/{owner}/{project}/runs/artifacts_lineage | Get runs artifacts lineage
[**impersonateToken**](RunsV1Api.md#impersonateToken) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/impersonate | Impersonate run token
[**invalidateRun**](RunsV1Api.md#invalidateRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/invalidate | Invalidate run
[**invalidateRuns**](RunsV1Api.md#invalidateRuns) | **POST** /api/v1/{owner}/{project}/runs/invalidate | Invalidate runs
[**listArchivedRuns**](RunsV1Api.md#listArchivedRuns) | **GET** /api/v1/archives/{user}/runs | List archived runs for user
[**listBookmarkedRuns**](RunsV1Api.md#listBookmarkedRuns) | **GET** /api/v1/bookmarks/{user}/runs | List bookmarked runs for user
[**listRuns**](RunsV1Api.md#listRuns) | **GET** /api/v1/{owner}/{project}/runs | List runs
[**listRunsIo**](RunsV1Api.md#listRunsIo) | **GET** /api/v1/{owner}/{project}/runs/io | List runs io
[**notifyRunStatus**](RunsV1Api.md#notifyRunStatus) | **POST** /streams/v1/{namespace}/{owner}/{project}/runs/{uuid}/notify | Notify run status
[**patchRun**](RunsV1Api.md#patchRun) | **PATCH** /api/v1/{owner}/{project}/runs/{run.uuid} | Patch run
[**restartRun**](RunsV1Api.md#restartRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/restart | Restart run
[**restoreRun**](RunsV1Api.md#restoreRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/restore | Restore run
[**resumeRun**](RunsV1Api.md#resumeRun) | **POST** /api/v1/{entity.owner}/{entity.project}/runs/{entity.uuid}/resume | Resume run
[**startRunTensorboard**](RunsV1Api.md#startRunTensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/start | Start run tensorboard
[**stopRun**](RunsV1Api.md#stopRun) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/stop | Stop run
[**stopRunTensorboard**](RunsV1Api.md#stopRunTensorboard) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/tensorboard/stop | Stop run tensorboard
[**stopRuns**](RunsV1Api.md#stopRuns) | **POST** /api/v1/{owner}/{project}/runs/stop | Stop runs
[**tagRuns**](RunsV1Api.md#tagRuns) | **POST** /api/v1/{owner}/{project}/runs/tag | Tag runs
[**unbookmarkRun**](RunsV1Api.md#unbookmarkRun) | **DELETE** /api/v1/{owner}/{project}/runs/{uuid}/unbookmark | Unbookmark run
[**updateRun**](RunsV1Api.md#updateRun) | **PUT** /api/v1/{owner}/{project}/runs/{run.uuid} | Update run
[**uploadRunArtifact**](RunsV1Api.md#uploadRunArtifact) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/artifacts/upload | Upload an artifact file to a store via run access
[**uploadRunLogs**](RunsV1Api.md#uploadRunLogs) | **POST** /api/v1/{owner}/{project}/runs/{uuid}/logs/upload | Upload a logs file to a store via run access


<a name="archiveRun"></a>
# **archiveRun**
> archiveRun(owner, project, uuid)

Archive run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.archiveRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#archiveRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="bookmarkRun"></a>
# **bookmarkRun**
> bookmarkRun(owner, project, uuid)

Bookmark run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.bookmarkRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#bookmarkRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="bookmarkRuns"></a>
# **bookmarkRuns**
> bookmarkRuns(owner, project, body)

Bookmark runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
    try {
      apiInstance.bookmarkRuns(owner, project, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#bookmarkRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="collectRunLogs"></a>
# **collectRunLogs**
> collectRunLogs(namespace, owner, project, uuid)

Collect run logs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | 
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.collectRunLogs(namespace, owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#collectRunLogs");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="copyRun"></a>
# **copyRun**
> V1Run copyRun(entityOwner, entityProject, entityUuid, body)

Restart run with copy

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String entityOwner = "entityOwner_example"; // String | Owner of the namespace
    String entityProject = "entityProject_example"; // String | Project
    String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
    V1Run body = new V1Run(); // V1Run | Run object
    try {
      V1Run result = apiInstance.copyRun(entityOwner, entityProject, entityUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#copyRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="createRun"></a>
# **createRun**
> V1Run createRun(owner, project, body)

Create new run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    V1OperationBody body = new V1OperationBody(); // V1OperationBody | operation object
    try {
      V1Run result = apiInstance.createRun(owner, project, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#createRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="createRunArtifactsLineage"></a>
# **createRunArtifactsLineage**
> createRunArtifactsLineage(owner, project, uuid, body)

Create bulk run run artifacts lineage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    V1RunArtifacts body = new V1RunArtifacts(); // V1RunArtifacts | Run Artifacts
    try {
      apiInstance.createRunArtifactsLineage(owner, project, uuid, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#createRunArtifactsLineage");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="createRunStatus"></a>
# **createRunStatus**
> V1Status createRunStatus(owner, project, uuid, body)

Create new run status

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    V1EntityStatusBodyRequest body = new V1EntityStatusBodyRequest(); // V1EntityStatusBodyRequest | 
    try {
      V1Status result = apiInstance.createRunStatus(owner, project, uuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#createRunStatus");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="deleteRun"></a>
# **deleteRun**
> deleteRun(owner, project, uuid)

Delete run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.deleteRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#deleteRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="deleteRunArtifactLineage"></a>
# **deleteRunArtifactLineage**
> deleteRunArtifactLineage(owner, project, uuid, name, namespace)

Delete run artifact lineage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    String name = "name_example"; // String | Artifact name
    String namespace = "namespace_example"; // String | namespace.
    try {
      apiInstance.deleteRunArtifactLineage(owner, project, uuid, name, namespace);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#deleteRunArtifactLineage");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="deleteRuns"></a>
# **deleteRuns**
> deleteRuns(owner, project, body)

Delete runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
    try {
      apiInstance.deleteRuns(owner, project, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#deleteRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getMultiRunEvents"></a>
# **getMultiRunEvents**
> V1EventsResponse getMultiRunEvents(namespace, owner, project, kind, names, runs, orient)

Get multi runs events

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | namespace
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String kind = "kind_example"; // String | The artifact kind
    String names = "names_example"; // String | Names query param.
    String runs = "runs_example"; // String | Runs query param.
    String orient = "orient_example"; // String | Orient query param.
    try {
      V1EventsResponse result = apiInstance.getMultiRunEvents(namespace, owner, project, kind, names, runs, orient);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getMultiRunEvents");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace |
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **kind** | **String**| The artifact kind | [enum: model, audio, video, histogram, image, tensor, dataframe, chart, csv, tsv, psv, ssv, metric, env, html, text, file, dir, dockerfile, docker_image, data, coderef, table, tensorboard, curve]
 **names** | **String**| Names query param. | [optional]
 **runs** | **String**| Runs query param. | [optional]
 **orient** | **String**| Orient query param. | [optional]

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRun"></a>
# **getRun**
> V1Run getRun(owner, project, uuid)

Get run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1Run result = apiInstance.getRun(owner, project, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunArtifact"></a>
# **getRunArtifact**
> String getRunArtifact(namespace, owner, project, uuid, path, stream)

Get run artifact

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
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
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |

<a name="getRunArtifactLineage"></a>
# **getRunArtifactLineage**
> V1RunArtifact getRunArtifactLineage(owner, project, uuid, name, namespace)

Get run artifacts lineage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    String name = "name_example"; // String | Artifact name
    String namespace = "namespace_example"; // String | namespace.
    try {
      V1RunArtifact result = apiInstance.getRunArtifactLineage(owner, project, uuid, name, namespace);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunArtifactLineage");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunArtifacts"></a>
# **getRunArtifacts**
> String getRunArtifacts(namespace, owner, project, uuid, path)

Get run artifacts

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
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
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |

<a name="getRunArtifactsLineage"></a>
# **getRunArtifactsLineage**
> V1ListRunArtifactsResponse getRunArtifactsLineage(owner, project, uuid, offset, limit, sort, query)

Get run artifacts lineage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    String uuid = "uuid_example"; // String | Entity uuid
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunArtifactsResponse result = apiInstance.getRunArtifactsLineage(owner, project, uuid, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunArtifactsLineage");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **uuid** | **String**| Entity uuid |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunArtifactsLineageNames"></a>
# **getRunArtifactsLineageNames**
> V1ListRunArtifactsResponse getRunArtifactsLineageNames(owner, project, uuid, offset, limit, sort, query)

Get run artifacts lineage names

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    String uuid = "uuid_example"; // String | Entity uuid
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunArtifactsResponse result = apiInstance.getRunArtifactsLineageNames(owner, project, uuid, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunArtifactsLineageNames");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **uuid** | **String**| Entity uuid |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunArtifactsTree"></a>
# **getRunArtifactsTree**
> V1ArtifactTree getRunArtifactsTree(namespace, owner, project, uuid, path)

Get run artifacts tree

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | namespace
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    String path = "path_example"; // String | Path query param.
    try {
      V1ArtifactTree result = apiInstance.getRunArtifactsTree(namespace, owner, project, uuid, path);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunArtifactsTree");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunEvents"></a>
# **getRunEvents**
> V1EventsResponse getRunEvents(namespace, owner, project, uuid, kind, names, orient)

Get run events

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | namespace
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    String kind = "kind_example"; // String | The artifact kind
    String names = "names_example"; // String | Names query param.
    String orient = "orient_example"; // String | Orient query param.
    try {
      V1EventsResponse result = apiInstance.getRunEvents(namespace, owner, project, uuid, kind, names, orient);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunEvents");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **namespace** | **String**| namespace |
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the run will be assigned |
 **uuid** | **String**| Uuid identifier of the entity |
 **kind** | **String**| The artifact kind | [enum: model, audio, video, histogram, image, tensor, dataframe, chart, csv, tsv, psv, ssv, metric, env, html, text, file, dir, dockerfile, docker_image, data, coderef, table, tensorboard, curve]
 **names** | **String**| Names query param. | [optional]
 **orient** | **String**| Orient query param. | [optional]

### Return type

[**V1EventsResponse**](V1EventsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunLogs"></a>
# **getRunLogs**
> V1Logs getRunLogs(namespace, owner, project, uuid, lastTime, lastFile)

Get run logs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | 
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    OffsetDateTime lastTime = new OffsetDateTime(); // OffsetDateTime | last time.
    String lastFile = "lastFile_example"; // String | last file.
    try {
      V1Logs result = apiInstance.getRunLogs(namespace, owner, project, uuid, lastTime, lastFile);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunLogs");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunNamespace"></a>
# **getRunNamespace**
> V1RunSettings getRunNamespace(owner, project, uuid)

Get Run namespace

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1RunSettings result = apiInstance.getRunNamespace(owner, project, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunNamespace");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunResources"></a>
# **getRunResources**
> V1EventsResponse getRunResources(namespace, owner, project, uuid, names, tail)

Get run resources events

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | namespace
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    String names = "names_example"; // String | Names query param.
    Boolean tail = true; // Boolean | Query param flag to tail the values.
    try {
      V1EventsResponse result = apiInstance.getRunResources(namespace, owner, project, uuid, names, tail);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunResources");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunSettings"></a>
# **getRunSettings**
> V1RunSettings getRunSettings(owner, project, uuid)

Get Run settings

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1RunSettings result = apiInstance.getRunSettings(owner, project, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunSettings");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunStatuses"></a>
# **getRunStatuses**
> V1Status getRunStatuses(owner, project, uuid)

Get run status

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1Status result = apiInstance.getRunStatuses(owner, project, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunStatuses");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="getRunsArtifactsLineage"></a>
# **getRunsArtifactsLineage**
> V1ListRunArtifactsResponse getRunsArtifactsLineage(owner, project, offset, limit, sort, query)

Get runs artifacts lineage

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunArtifactsResponse result = apiInstance.getRunsArtifactsLineage(owner, project, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#getRunsArtifactsLineage");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

[**V1ListRunArtifactsResponse**](V1ListRunArtifactsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="impersonateToken"></a>
# **impersonateToken**
> V1Auth impersonateToken(owner, project, uuid)

Impersonate run token

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      V1Auth result = apiInstance.impersonateToken(owner, project, uuid);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#impersonateToken");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="invalidateRun"></a>
# **invalidateRun**
> invalidateRun(owner, project, uuid)

Invalidate run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.invalidateRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#invalidateRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="invalidateRuns"></a>
# **invalidateRuns**
> invalidateRuns(owner, project, body)

Invalidate runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
    try {
      apiInstance.invalidateRuns(owner, project, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#invalidateRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listArchivedRuns"></a>
# **listArchivedRuns**
> V1ListRunsResponse listArchivedRuns(user, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String user = "user_example"; // String | User
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunsResponse result = apiInstance.listArchivedRuns(user, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#listArchivedRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listBookmarkedRuns"></a>
# **listBookmarkedRuns**
> V1ListRunsResponse listBookmarkedRuns(user, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String user = "user_example"; // String | User
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunsResponse result = apiInstance.listBookmarkedRuns(user, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#listBookmarkedRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listRuns"></a>
# **listRuns**
> V1ListRunsResponse listRuns(owner, project, offset, limit, sort, query)

List runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunsResponse result = apiInstance.listRuns(owner, project, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#listRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="listRunsIo"></a>
# **listRunsIo**
> V1ListRunsResponse listRunsIo(owner, project, offset, limit, sort, query)

List runs io

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    Integer offset = 56; // Integer | Pagination offset.
    Integer limit = 56; // Integer | Limit size.
    String sort = "sort_example"; // String | Sort to order the search.
    String query = "query_example"; // String | Query filter the search search.
    try {
      V1ListRunsResponse result = apiInstance.listRunsIo(owner, project, offset, limit, sort, query);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#listRunsIo");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="notifyRunStatus"></a>
# **notifyRunStatus**
> notifyRunStatus(namespace, owner, project, uuid, body)

Notify run status

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String namespace = "namespace_example"; // String | Na,espace
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    V1EntityNotificationBody body = new V1EntityNotificationBody(); // V1EntityNotificationBody | 
    try {
      apiInstance.notifyRunStatus(namespace, owner, project, uuid, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#notifyRunStatus");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="patchRun"></a>
# **patchRun**
> V1Run patchRun(owner, project, runUuid, body)

Patch run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String runUuid = "runUuid_example"; // String | UUID
    V1Run body = new V1Run(); // V1Run | Run object
    try {
      V1Run result = apiInstance.patchRun(owner, project, runUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#patchRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="restartRun"></a>
# **restartRun**
> V1Run restartRun(entityOwner, entityProject, entityUuid, body)

Restart run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String entityOwner = "entityOwner_example"; // String | Owner of the namespace
    String entityProject = "entityProject_example"; // String | Project
    String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
    V1Run body = new V1Run(); // V1Run | Run object
    try {
      V1Run result = apiInstance.restartRun(entityOwner, entityProject, entityUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#restartRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="restoreRun"></a>
# **restoreRun**
> restoreRun(owner, project, uuid)

Restore run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.restoreRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#restoreRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="resumeRun"></a>
# **resumeRun**
> V1Run resumeRun(entityOwner, entityProject, entityUuid, body)

Resume run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String entityOwner = "entityOwner_example"; // String | Owner of the namespace
    String entityProject = "entityProject_example"; // String | Project
    String entityUuid = "entityUuid_example"; // String | Uuid identifier of the entity
    V1Run body = new V1Run(); // V1Run | Run object
    try {
      V1Run result = apiInstance.resumeRun(entityOwner, entityProject, entityUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#resumeRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="startRunTensorboard"></a>
# **startRunTensorboard**
> startRunTensorboard(owner, project, uuid, body)

Start run tensorboard

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    V1ProjectEntityResourceRequest body = new V1ProjectEntityResourceRequest(); // V1ProjectEntityResourceRequest | 
    try {
      apiInstance.startRunTensorboard(owner, project, uuid, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#startRunTensorboard");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="stopRun"></a>
# **stopRun**
> stopRun(owner, project, uuid)

Stop run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.stopRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#stopRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="stopRunTensorboard"></a>
# **stopRunTensorboard**
> stopRunTensorboard(owner, project, uuid)

Stop run tensorboard

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.stopRunTensorboard(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#stopRunTensorboard");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="stopRuns"></a>
# **stopRuns**
> stopRuns(owner, project, body)

Stop runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    V1Uuids body = new V1Uuids(); // V1Uuids | Uuids of the entities
    try {
      apiInstance.stopRuns(owner, project, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#stopRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="tagRuns"></a>
# **tagRuns**
> tagRuns(owner, project, body)

Tag runs

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project under namesapce
    V1EntitiesTags body = new V1EntitiesTags(); // V1EntitiesTags | Data
    try {
      apiInstance.tagRuns(owner, project, body);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#tagRuns");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **body** | [**V1EntitiesTags**](V1EntitiesTags.md)| Data |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="unbookmarkRun"></a>
# **unbookmarkRun**
> unbookmarkRun(owner, project, uuid)

Unbookmark run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project
    String uuid = "uuid_example"; // String | Uuid identifier of the entity
    try {
      apiInstance.unbookmarkRun(owner, project, uuid);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#unbookmarkRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="updateRun"></a>
# **updateRun**
> V1Run updateRun(owner, project, runUuid, body)

Update run

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project where the run will be assigned
    String runUuid = "runUuid_example"; // String | UUID
    V1Run body = new V1Run(); // V1Run | Run object
    try {
      V1Run result = apiInstance.updateRun(owner, project, runUuid, body);
      System.out.println(result);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#updateRun");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |
**0** | An unexpected error response |  -  |

<a name="uploadRunArtifact"></a>
# **uploadRunArtifact**
> uploadRunArtifact(owner, project, uuid, uploadfile, path, overwrite)

Upload an artifact file to a store via run access

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project having access to the store
    String uuid = "uuid_example"; // String | Unique integer identifier of the entity
    File uploadfile = new File("/path/to/file"); // File | The file to upload.
    String path = "path_example"; // String | File path query params.
    Boolean overwrite = true; // Boolean | File path query params.
    try {
      apiInstance.uploadRunArtifact(owner, project, uuid, uploadfile, path, overwrite);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#uploadRunArtifact");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |

<a name="uploadRunLogs"></a>
# **uploadRunLogs**
> uploadRunLogs(owner, project, uuid, uploadfile, path, overwrite)

Upload a logs file to a store via run access

### Example
```java
// Import classes:
import org.openapitools.client.ApiClient;
import org.openapitools.client.ApiException;
import org.openapitools.client.Configuration;
import org.openapitools.client.auth.*;
import org.openapitools.client.models.*;
import org.openapitools.client.api.RunsV1Api;

public class Example {
  public static void main(String[] args) {
    ApiClient defaultClient = Configuration.getDefaultApiClient();
    defaultClient.setBasePath("http://localhost");
    
    // Configure API key authorization: ApiKey
    ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
    ApiKey.setApiKey("YOUR API KEY");
    // Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
    //ApiKey.setApiKeyPrefix("Token");

    RunsV1Api apiInstance = new RunsV1Api(defaultClient);
    String owner = "owner_example"; // String | Owner of the namespace
    String project = "project_example"; // String | Project having access to the store
    String uuid = "uuid_example"; // String | Unique integer identifier of the entity
    File uploadfile = new File("/path/to/file"); // File | The file to upload.
    String path = "path_example"; // String | File path query params.
    Boolean overwrite = true; // Boolean | File path query params.
    try {
      apiInstance.uploadRunLogs(owner, project, uuid, uploadfile, path, overwrite);
    } catch (ApiException e) {
      System.err.println("Exception when calling RunsV1Api#uploadRunLogs");
      System.err.println("Status code: " + e.getCode());
      System.err.println("Reason: " + e.getResponseBody());
      System.err.println("Response headers: " + e.getResponseHeaders());
      e.printStackTrace();
    }
  }
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

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response. |  -  |
**204** | No content. |  -  |
**403** | You don&#39;t have permission to access the resource. |  -  |
**404** | Resource does not exist. |  -  |


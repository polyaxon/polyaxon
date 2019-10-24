# RunsV1Api

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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.archiveRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#archiveRun");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.bookmarkRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#bookmarkRun");
    e.printStackTrace();
}
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
> V1Run copyRun(entityOwner, entityProject, entityUuid, body)

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
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityUuid = "entityUuid_example"; // String | Unique integer identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.copyRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#copyRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project where the experiement will be assigned |
 **entityUuid** | **String**| Unique integer identifier of the entity |
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
String project = "project_example"; // String | Project where the experiement will be assigned
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.createRun(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#createRun");
    e.printStackTrace();
}
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
> V1CodeReference createRunCodeRef(entityOwner, entityProject, entityUuid, body)

Get run code ref

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
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityUuid = "entityUuid_example"; // String | Unique integer identifier of the entity
V1CodeReference body = new V1CodeReference(); // V1CodeReference | Code ref object
try {
    V1CodeReference result = apiInstance.createRunCodeRef(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#createRunCodeRef");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project where the experiement will be assigned |
 **entityUuid** | **String**| Unique integer identifier of the entity |
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
V1EntityStatusBodyRequest body = new V1EntityStatusBodyRequest(); // V1EntityStatusBodyRequest | 
try {
    V1Status result = apiInstance.createRunStatus(owner, project, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#createRunStatus");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#deleteRun");
    e.printStackTrace();
}
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
    Object result = apiInstance.deleteRuns(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#deleteRuns");
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Run result = apiInstance.getRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#getRun");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1ListCodeRefsResponse result = apiInstance.getRunCodeRefs(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#getRunCodeRefs");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Status result = apiInstance.getRunStatuses(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#getRunStatuses");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Auth result = apiInstance.impersonateToken(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#impersonateToken");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
V1EntityResourceRequest body = new V1EntityResourceRequest(); // V1EntityResourceRequest | 
try {
    Object result = apiInstance.invalidateRun(owner, project, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#invalidateRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **uuid** | **String**| Unique integer identifier of the entity |
 **body** | [**V1EntityResourceRequest**](V1EntityResourceRequest.md)|  |

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
    Object result = apiInstance.invalidateRuns(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#invalidateRuns");
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

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listArchivedRuns"></a>
# **listArchivedRuns**
> V1ListRunsResponse listArchivedRuns(user, offset, limit, sort, query)

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
    V1ListRunsResponse result = apiInstance.listArchivedRuns(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#listArchivedRuns");
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

<a name="listBookmarkedRuns"></a>
# **listBookmarkedRuns**
> V1ListRunsResponse listBookmarkedRuns(user, offset, limit, sort, query)

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
    V1ListRunsResponse result = apiInstance.listBookmarkedRuns(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#listBookmarkedRuns");
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

<a name="listRuns"></a>
# **listRuns**
> V1ListRunsResponse listRuns(owner, project, offset, limit, sort, query)

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
    V1ListRunsResponse result = apiInstance.listRuns(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#listRuns");
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

<a name="patchRun"></a>
# **patchRun**
> V1Run patchRun(owner, project, runUuid, body)

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
String project = "project_example"; // String | Project where the experiement will be assigned
String runUuid = "runUuid_example"; // String | UUID
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.patchRun(owner, project, runUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#patchRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **runUuid** | **String**| UUID |
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
> V1Run restartRun(entityOwner, entityProject, entityUuid, body)

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
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityUuid = "entityUuid_example"; // String | Unique integer identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.restartRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#restartRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project where the experiement will be assigned |
 **entityUuid** | **String**| Unique integer identifier of the entity |
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.restoreRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#restoreRun");
    e.printStackTrace();
}
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
> V1Run resumeRun(entityOwner, entityProject, entityUuid, body)

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
String entityProject = "entityProject_example"; // String | Project where the experiement will be assigned
String entityUuid = "entityUuid_example"; // String | Unique integer identifier of the entity
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.resumeRun(entityOwner, entityProject, entityUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#resumeRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entityOwner** | **String**| Owner of the namespace |
 **entityProject** | **String**| Project where the experiement will be assigned |
 **entityUuid** | **String**| Unique integer identifier of the entity |
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
V1EntityResourceRequest body = new V1EntityResourceRequest(); // V1EntityResourceRequest | 
try {
    Object result = apiInstance.startRunTensorboard(owner, project, uuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#startRunTensorboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **uuid** | **String**| Unique integer identifier of the entity |
 **body** | [**V1EntityResourceRequest**](V1EntityResourceRequest.md)|  |

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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.stopRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#stopRun");
    e.printStackTrace();
}
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.stopRunTensorboard(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#stopRunTensorboard");
    e.printStackTrace();
}
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
    Object result = apiInstance.stopRuns(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#stopRuns");
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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.unbookmarkRun(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#unbookmarkRun");
    e.printStackTrace();
}
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
> V1Run updateRun(owner, project, runUuid, body)

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
String project = "project_example"; // String | Project where the experiement will be assigned
String runUuid = "runUuid_example"; // String | UUID
V1Run body = new V1Run(); // V1Run | Run object
try {
    V1Run result = apiInstance.updateRun(owner, project, runUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunsV1Api#updateRun");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project where the experiement will be assigned |
 **runUuid** | **String**| UUID |
 **body** | [**V1Run**](V1Run.md)| Run object |

### Return type

[**V1Run**](V1Run.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


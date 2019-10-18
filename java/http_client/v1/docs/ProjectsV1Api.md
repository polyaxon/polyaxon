# ProjectsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**archiveProject**](ProjectsV1Api.md#archiveProject) | **POST** /api/v1/{owner}/{project}/archive | Stop run
[**bookmarkProject**](ProjectsV1Api.md#bookmarkProject) | **POST** /api/v1/{owner}/{project}/bookmark | Stop run
[**createProject**](ProjectsV1Api.md#createProject) | **POST** /api/v1/{owner}/projects/create | Get run
[**deleteProject**](ProjectsV1Api.md#deleteProject) | **DELETE** /api/v1/{owner}/projecs/{project} | Delete runs
[**disableProjectCI**](ProjectsV1Api.md#disableProjectCI) | **DELETE** /api/v1/{owner}/{project}/ci | Restart run
[**enableProjectCI**](ProjectsV1Api.md#enableProjectCI) | **POST** /api/v1/{owner}/{project}/ci | Restart run with copy
[**getProject**](ProjectsV1Api.md#getProject) | **GET** /api/v1/{owner}/projects/{project} | Update run
[**listArchivedProjects**](ProjectsV1Api.md#listArchivedProjects) | **GET** /api/v1/archives/{user}/projects | Create new run
[**listBookmarkedProjects**](ProjectsV1Api.md#listBookmarkedProjects) | **GET** /api/v1/bookmarks/{user}/projects | List archived runs for user
[**listProjectNames**](ProjectsV1Api.md#listProjectNames) | **GET** /api/v1/{owner}/projects/names | List bookmarked runs for user
[**listProjects**](ProjectsV1Api.md#listProjects) | **GET** /api/v1/{owner}/projects/list | List runs
[**patchProject**](ProjectsV1Api.md#patchProject) | **PATCH** /api/v1/{owner}/projects/{project} | Delete run
[**restoreExperiment**](ProjectsV1Api.md#restoreExperiment) | **POST** /api/v1/{owner}/{project}/restore | Stop runs
[**unbookmarkProject**](ProjectsV1Api.md#unbookmarkProject) | **DELETE** /api/v1/{owner}/{project}/unbookmark | Invalidate runs
[**updateProject**](ProjectsV1Api.md#updateProject) | **PUT** /api/v1/{owner}/projects/{project} | Patch run


<a name="archiveProject"></a>
# **archiveProject**
> Object archiveProject(owner, project)

Stop run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.archiveProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#archiveProject");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.bookmarkProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#bookmarkProject");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1OwnerBodyRequest body = new V1OwnerBodyRequest(); // V1OwnerBodyRequest | 
try {
    V1Project result = apiInstance.createProject(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#createProject");
    e.printStackTrace();
}
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

<a name="deleteProject"></a>
# **deleteProject**
> Object deleteProject(owner, project)

Delete runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.deleteProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#deleteProject");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.disableProjectCI(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#disableProjectCI");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.enableProjectCI(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#enableProjectCI");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    V1Project result = apiInstance.getProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#getProject");
    e.printStackTrace();
}
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
> V1ListProjectsResponse listArchivedProjects(user, page, limit, sort, query)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String user = "user_example"; // String | User
String page = "page_example"; // String | Pagination.
String limit = "limit_example"; // String | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.listArchivedProjects(user, page, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#listArchivedProjects");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User |
 **page** | **String**| Pagination. | [optional]
 **limit** | **String**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listBookmarkedProjects"></a>
# **listBookmarkedProjects**
> V1ListProjectsResponse listBookmarkedProjects(user, page, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String user = "user_example"; // String | User
String page = "page_example"; // String | Pagination.
String limit = "limit_example"; // String | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.listBookmarkedProjects(user, page, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#listBookmarkedProjects");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User |
 **page** | **String**| Pagination. | [optional]
 **limit** | **String**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectNames"></a>
# **listProjectNames**
> V1ListProjectsResponse listProjectNames(owner, page, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String page = "page_example"; // String | Pagination.
String limit = "limit_example"; // String | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.listProjectNames(owner, page, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#listProjectNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **page** | **String**| Pagination. | [optional]
 **limit** | **String**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjects"></a>
# **listProjects**
> V1ListProjectsResponse listProjects(owner, page, limit, sort, query)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String page = "page_example"; // String | Pagination.
String limit = "limit_example"; // String | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.listProjects(owner, page, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#listProjects");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **page** | **String**| Pagination. | [optional]
 **limit** | **String**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1ProjectBodyRequest body = new V1ProjectBodyRequest(); // V1ProjectBodyRequest | 
try {
    V1Project result = apiInstance.patchProject(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#patchProject");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.restoreExperiment(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#restoreExperiment");
    e.printStackTrace();
}
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

<a name="unbookmarkProject"></a>
# **unbookmarkProject**
> Object unbookmarkProject(owner, project)

Invalidate runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
try {
    Object result = apiInstance.unbookmarkProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#unbookmarkProject");
    e.printStackTrace();
}
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
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectsV1Api apiInstance = new ProjectsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1ProjectBodyRequest body = new V1ProjectBodyRequest(); // V1ProjectBodyRequest | 
try {
    V1Project result = apiInstance.updateProject(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#updateProject");
    e.printStackTrace();
}
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


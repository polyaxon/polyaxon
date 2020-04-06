# ProjectsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projectsV1ArchiveProject**](ProjectsV1Api.md#projectsV1ArchiveProject) | **POST** /api/v1/{owner}/{project}/archive | Archive project
[**projectsV1BookmarkProject**](ProjectsV1Api.md#projectsV1BookmarkProject) | **POST** /api/v1/{owner}/{project}/bookmark | Bookmark project
[**projectsV1CreateProject**](ProjectsV1Api.md#projectsV1CreateProject) | **POST** /api/v1/{owner}/projects/create | Create new project
[**projectsV1DeleteProject**](ProjectsV1Api.md#projectsV1DeleteProject) | **DELETE** /api/v1/{owner}/{project} | Delete project
[**projectsV1DisableProjectCI**](ProjectsV1Api.md#projectsV1DisableProjectCI) | **DELETE** /api/v1/{owner}/{project}/ci | Disbale project CI
[**projectsV1EnableProjectCI**](ProjectsV1Api.md#projectsV1EnableProjectCI) | **POST** /api/v1/{owner}/{project}/ci | Enable project CI
[**projectsV1FetchProjectTeams**](ProjectsV1Api.md#projectsV1FetchProjectTeams) | **GET** /api/v1/{owner}/{project}/teams | Get project teams
[**projectsV1GetProject**](ProjectsV1Api.md#projectsV1GetProject) | **GET** /api/v1/{owner}/{project} | Get project
[**projectsV1GetProjectSettings**](ProjectsV1Api.md#projectsV1GetProjectSettings) | **GET** /api/v1/{owner}/{project}/settings | Get Project settings
[**projectsV1ListArchivedProjects**](ProjectsV1Api.md#projectsV1ListArchivedProjects) | **GET** /api/v1/archives/{user}/projects | List archived projects for user
[**projectsV1ListBookmarkedProjects**](ProjectsV1Api.md#projectsV1ListBookmarkedProjects) | **GET** /api/v1/bookmarks/{user}/projects | List bookmarked projects for user
[**projectsV1ListProjectNames**](ProjectsV1Api.md#projectsV1ListProjectNames) | **GET** /api/v1/{owner}/projects/names | List project names
[**projectsV1ListProjects**](ProjectsV1Api.md#projectsV1ListProjects) | **GET** /api/v1/{owner}/projects/list | List projects
[**projectsV1PatchProject**](ProjectsV1Api.md#projectsV1PatchProject) | **PATCH** /api/v1/{owner}/{project.name} | Patch project
[**projectsV1PatchProjectSettings**](ProjectsV1Api.md#projectsV1PatchProjectSettings) | **PATCH** /api/v1/{owner}/{project}/settings | Patch project settings
[**projectsV1PatchProjectTeams**](ProjectsV1Api.md#projectsV1PatchProjectTeams) | **PATCH** /api/v1/{owner}/{project}/teams | Patch project teams
[**projectsV1RestoreProject**](ProjectsV1Api.md#projectsV1RestoreProject) | **POST** /api/v1/{owner}/{project}/restore | Restore project
[**projectsV1UnbookmarkProject**](ProjectsV1Api.md#projectsV1UnbookmarkProject) | **DELETE** /api/v1/{owner}/{project}/unbookmark | Unbookmark project
[**projectsV1UpdateProject**](ProjectsV1Api.md#projectsV1UpdateProject) | **PUT** /api/v1/{owner}/{project.name} | Update project
[**projectsV1UpdateProjectSettings**](ProjectsV1Api.md#projectsV1UpdateProjectSettings) | **PUT** /api/v1/{owner}/{project}/settings | Update project settings
[**projectsV1UpdateProjectTeams**](ProjectsV1Api.md#projectsV1UpdateProjectTeams) | **PUT** /api/v1/{owner}/{project}/teams | Update project teams
[**uploadProjectArtifact**](ProjectsV1Api.md#uploadProjectArtifact) | **POST** /api/v1/{owner}/{project}/artifacts/{uuid}/upload | Upload artifact to a store via project access


<a name="projectsV1ArchiveProject"></a>
# **projectsV1ArchiveProject**
> projectsV1ArchiveProject(owner, project)

Archive project

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
    apiInstance.projectsV1ArchiveProject(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1ArchiveProject");
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

<a name="projectsV1BookmarkProject"></a>
# **projectsV1BookmarkProject**
> projectsV1BookmarkProject(owner, project)

Bookmark project

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
    apiInstance.projectsV1BookmarkProject(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1BookmarkProject");
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

<a name="projectsV1CreateProject"></a>
# **projectsV1CreateProject**
> V1Project projectsV1CreateProject(owner, body)

Create new project

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
V1Project body = new V1Project(); // V1Project | Project body
try {
    V1Project result = apiInstance.projectsV1CreateProject(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1CreateProject");
    e.printStackTrace();
}
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

<a name="projectsV1DeleteProject"></a>
# **projectsV1DeleteProject**
> projectsV1DeleteProject(owner, project)

Delete project

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
    apiInstance.projectsV1DeleteProject(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1DeleteProject");
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

<a name="projectsV1DisableProjectCI"></a>
# **projectsV1DisableProjectCI**
> projectsV1DisableProjectCI(owner, project)

Disbale project CI

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
    apiInstance.projectsV1DisableProjectCI(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1DisableProjectCI");
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

<a name="projectsV1EnableProjectCI"></a>
# **projectsV1EnableProjectCI**
> projectsV1EnableProjectCI(owner, project)

Enable project CI

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
    apiInstance.projectsV1EnableProjectCI(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1EnableProjectCI");
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

<a name="projectsV1FetchProjectTeams"></a>
# **projectsV1FetchProjectTeams**
> V1ProjectTeams projectsV1FetchProjectTeams(owner, project)

Get project teams

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
    V1ProjectTeams result = apiInstance.projectsV1FetchProjectTeams(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1FetchProjectTeams");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |

### Return type

[**V1ProjectTeams**](V1ProjectTeams.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1GetProject"></a>
# **projectsV1GetProject**
> V1Project projectsV1GetProject(owner, project)

Get project

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
    V1Project result = apiInstance.projectsV1GetProject(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1GetProject");
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

<a name="projectsV1GetProjectSettings"></a>
# **projectsV1GetProjectSettings**
> V1ProjectSettings projectsV1GetProjectSettings(owner, project)

Get Project settings

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
    V1ProjectSettings result = apiInstance.projectsV1GetProjectSettings(owner, project);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1GetProjectSettings");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |

### Return type

[**V1ProjectSettings**](V1ProjectSettings.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1ListArchivedProjects"></a>
# **projectsV1ListArchivedProjects**
> V1ListProjectsResponse projectsV1ListArchivedProjects(user, offset, limit, sort, query)

List archived projects for user

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.projectsV1ListArchivedProjects(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1ListArchivedProjects");
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

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1ListBookmarkedProjects"></a>
# **projectsV1ListBookmarkedProjects**
> V1ListProjectsResponse projectsV1ListBookmarkedProjects(user, offset, limit, sort, query)

List bookmarked projects for user

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.projectsV1ListBookmarkedProjects(user, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1ListBookmarkedProjects");
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

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1ListProjectNames"></a>
# **projectsV1ListProjectNames**
> V1ListProjectsResponse projectsV1ListProjectNames(owner, offset, limit, sort, query)

List project names

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.projectsV1ListProjectNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1ListProjectNames");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1ListProjects"></a>
# **projectsV1ListProjects**
> V1ListProjectsResponse projectsV1ListProjects(owner, offset, limit, sort, query)

List projects

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
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListProjectsResponse result = apiInstance.projectsV1ListProjects(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1ListProjects");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **offset** | **Integer**| Pagination offset. | [optional]
 **limit** | **Integer**| Limit size. | [optional]
 **sort** | **String**| Sort to order the search. | [optional]
 **query** | **String**| Query filter the search search. | [optional]

### Return type

[**V1ListProjectsResponse**](V1ListProjectsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1PatchProject"></a>
# **projectsV1PatchProject**
> V1Project projectsV1PatchProject(owner, projectName, body)

Patch project

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
String projectName = "projectName_example"; // String | Required name
V1Project body = new V1Project(); // V1Project | Project body
try {
    V1Project result = apiInstance.projectsV1PatchProject(owner, projectName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1PatchProject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **projectName** | **String**| Required name |
 **body** | [**V1Project**](V1Project.md)| Project body |

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1PatchProjectSettings"></a>
# **projectsV1PatchProjectSettings**
> V1ProjectSettings projectsV1PatchProjectSettings(owner, project, body)

Patch project settings

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
String project = "project_example"; // String | Project name
V1ProjectSettings body = new V1ProjectSettings(); // V1ProjectSettings | Project settings body
try {
    V1ProjectSettings result = apiInstance.projectsV1PatchProjectSettings(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1PatchProjectSettings");
    e.printStackTrace();
}
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

<a name="projectsV1PatchProjectTeams"></a>
# **projectsV1PatchProjectTeams**
> V1ProjectTeams projectsV1PatchProjectTeams(owner, project, body)

Patch project teams

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
String project = "project_example"; // String | Project name
V1ProjectTeams body = new V1ProjectTeams(); // V1ProjectTeams | Project settings body
try {
    V1ProjectTeams result = apiInstance.projectsV1PatchProjectTeams(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1PatchProjectTeams");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project name |
 **body** | [**V1ProjectTeams**](V1ProjectTeams.md)| Project settings body |

### Return type

[**V1ProjectTeams**](V1ProjectTeams.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1RestoreProject"></a>
# **projectsV1RestoreProject**
> projectsV1RestoreProject(owner, project)

Restore project

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
    apiInstance.projectsV1RestoreProject(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1RestoreProject");
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

<a name="projectsV1UnbookmarkProject"></a>
# **projectsV1UnbookmarkProject**
> projectsV1UnbookmarkProject(owner, project)

Unbookmark project

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
    apiInstance.projectsV1UnbookmarkProject(owner, project);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1UnbookmarkProject");
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

<a name="projectsV1UpdateProject"></a>
# **projectsV1UpdateProject**
> V1Project projectsV1UpdateProject(owner, projectName, body)

Update project

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
String projectName = "projectName_example"; // String | Required name
V1Project body = new V1Project(); // V1Project | Project body
try {
    V1Project result = apiInstance.projectsV1UpdateProject(owner, projectName, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1UpdateProject");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **projectName** | **String**| Required name |
 **body** | [**V1Project**](V1Project.md)| Project body |

### Return type

[**V1Project**](V1Project.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectsV1UpdateProjectSettings"></a>
# **projectsV1UpdateProjectSettings**
> V1ProjectSettings projectsV1UpdateProjectSettings(owner, project, body)

Update project settings

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
String project = "project_example"; // String | Project name
V1ProjectSettings body = new V1ProjectSettings(); // V1ProjectSettings | Project settings body
try {
    V1ProjectSettings result = apiInstance.projectsV1UpdateProjectSettings(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1UpdateProjectSettings");
    e.printStackTrace();
}
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

<a name="projectsV1UpdateProjectTeams"></a>
# **projectsV1UpdateProjectTeams**
> V1ProjectTeams projectsV1UpdateProjectTeams(owner, project, body)

Update project teams

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
String project = "project_example"; // String | Project name
V1ProjectTeams body = new V1ProjectTeams(); // V1ProjectTeams | Project settings body
try {
    V1ProjectTeams result = apiInstance.projectsV1UpdateProjectTeams(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#projectsV1UpdateProjectTeams");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project name |
 **body** | [**V1ProjectTeams**](V1ProjectTeams.md)| Project settings body |

### Return type

[**V1ProjectTeams**](V1ProjectTeams.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="uploadProjectArtifact"></a>
# **uploadProjectArtifact**
> uploadProjectArtifact(owner, project, uuid, uploadfile, path, overwrite)

Upload artifact to a store via project access

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
String project = "project_example"; // String | Project having access to the store
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
File uploadfile = new File("/path/to/file.txt"); // File | The file to upload.
String path = "path_example"; // String | File path query params.
Boolean overwrite = true; // Boolean | File path query params.
try {
    apiInstance.uploadProjectArtifact(owner, project, uuid, uploadfile, path, overwrite);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectsV1Api#uploadProjectArtifact");
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


# ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projectDashboardsV1CreateProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1CreateProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards | Create project dashboard
[**projectDashboardsV1DeleteProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1DeleteProjectDashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Delete project dashboard
[**projectDashboardsV1GetProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1GetProjectDashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Get project dashboard
[**projectDashboardsV1ListProjectDashboardNames**](ProjectDashboardsV1Api.md#projectDashboardsV1ListProjectDashboardNames) | **GET** /api/v1/{owner}/{project}/dashboards/names | List project dashboard
[**projectDashboardsV1ListProjectDashboards**](ProjectDashboardsV1Api.md#projectDashboardsV1ListProjectDashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List project dashboards
[**projectDashboardsV1PatchProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1PatchProjectDashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Patch project dashboard
[**projectDashboardsV1PromoteProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1PromoteProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Promote project dashboard
[**projectDashboardsV1UpdateProjectDashboard**](ProjectDashboardsV1Api.md#projectDashboardsV1UpdateProjectDashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update project dashboard


<a name="projectDashboardsV1CreateProjectDashboard"></a>
# **projectDashboardsV1CreateProjectDashboard**
> V1Dashboard projectDashboardsV1CreateProjectDashboard(owner, project, body)

Create project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.projectDashboardsV1CreateProjectDashboard(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1CreateProjectDashboard");
    e.printStackTrace();
}
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

<a name="projectDashboardsV1DeleteProjectDashboard"></a>
# **projectDashboardsV1DeleteProjectDashboard**
> projectDashboardsV1DeleteProjectDashboard(owner, project, uuid)

Delete project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.projectDashboardsV1DeleteProjectDashboard(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1DeleteProjectDashboard");
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

<a name="projectDashboardsV1GetProjectDashboard"></a>
# **projectDashboardsV1GetProjectDashboard**
> V1Dashboard projectDashboardsV1GetProjectDashboard(owner, project, uuid)

Get project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Dashboard result = apiInstance.projectDashboardsV1GetProjectDashboard(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1GetProjectDashboard");
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

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1ListProjectDashboardNames"></a>
# **projectDashboardsV1ListProjectDashboardNames**
> V1ListDashboardsResponse projectDashboardsV1ListProjectDashboardNames(owner, project, offset, limit, sort, query)

List project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListDashboardsResponse result = apiInstance.projectDashboardsV1ListProjectDashboardNames(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1ListProjectDashboardNames");
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1ListProjectDashboards"></a>
# **projectDashboardsV1ListProjectDashboards**
> V1ListDashboardsResponse projectDashboardsV1ListProjectDashboards(owner, project, offset, limit, sort, query)

List project dashboards

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListDashboardsResponse result = apiInstance.projectDashboardsV1ListProjectDashboards(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1ListProjectDashboards");
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1PatchProjectDashboard"></a>
# **projectDashboardsV1PatchProjectDashboard**
> V1Dashboard projectDashboardsV1PatchProjectDashboard(owner, project, dashboardUuid, body)

Patch project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String dashboardUuid = "dashboardUuid_example"; // String | UUID
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.projectDashboardsV1PatchProjectDashboard(owner, project, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1PatchProjectDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **dashboardUuid** | **String**| UUID |
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1PromoteProjectDashboard"></a>
# **projectDashboardsV1PromoteProjectDashboard**
> V1Dashboard projectDashboardsV1PromoteProjectDashboard(owner, project, dashboardUuid)

Promote project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String dashboardUuid = "dashboardUuid_example"; // String | UUID
try {
    V1Dashboard result = apiInstance.projectDashboardsV1PromoteProjectDashboard(owner, project, dashboardUuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1PromoteProjectDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **dashboardUuid** | **String**| UUID |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectDashboardsV1UpdateProjectDashboard"></a>
# **projectDashboardsV1UpdateProjectDashboard**
> V1Dashboard projectDashboardsV1UpdateProjectDashboard(owner, project, dashboardUuid, body)

Update project dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectDashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectDashboardsV1Api apiInstance = new ProjectDashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String dashboardUuid = "dashboardUuid_example"; // String | UUID
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.projectDashboardsV1UpdateProjectDashboard(owner, project, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#projectDashboardsV1UpdateProjectDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **dashboardUuid** | **String**| UUID |
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


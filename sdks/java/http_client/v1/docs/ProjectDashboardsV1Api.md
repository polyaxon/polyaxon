# ProjectDashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createProjectDashboard**](ProjectDashboardsV1Api.md#createProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards | List runs
[**deleteProjectDashboard**](ProjectDashboardsV1Api.md#deleteProjectDashboard) | **DELETE** /api/v1/{owner}/{project}/dashboards/{uuid} | Patch run
[**getProjectDashboard**](ProjectDashboardsV1Api.md#getProjectDashboard) | **GET** /api/v1/{owner}/{project}/dashboards/{uuid} | Create new run
[**listProjectDashboardNames**](ProjectDashboardsV1Api.md#listProjectDashboardNames) | **GET** /api/v1/{owner}/{project}/dashboards/names | List bookmarked runs for user
[**listProjectDashboards**](ProjectDashboardsV1Api.md#listProjectDashboards) | **GET** /api/v1/{owner}/{project}/dashboards | List archived runs for user
[**patchProjectDashboard**](ProjectDashboardsV1Api.md#patchProjectDashboard) | **PATCH** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Update run
[**promoteProjectDashboard**](ProjectDashboardsV1Api.md#promoteProjectDashboard) | **POST** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid}/promote | Delete run
[**updateProjectDashboard**](ProjectDashboardsV1Api.md#updateProjectDashboard) | **PUT** /api/v1/{owner}/{project}/dashboards/{dashboard.uuid} | Get run


<a name="createProjectDashboard"></a>
# **createProjectDashboard**
> V1Dashboard createProjectDashboard(owner, project, body)

List runs

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
    V1Dashboard result = apiInstance.createProjectDashboard(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#createProjectDashboard");
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

<a name="deleteProjectDashboard"></a>
# **deleteProjectDashboard**
> deleteProjectDashboard(owner, project, uuid)

Patch run

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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteProjectDashboard(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#deleteProjectDashboard");
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

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getProjectDashboard"></a>
# **getProjectDashboard**
> V1Dashboard getProjectDashboard(owner, project, uuid)

Create new run

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
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Dashboard result = apiInstance.getProjectDashboard(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#getProjectDashboard");
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

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listProjectDashboardNames"></a>
# **listProjectDashboardNames**
> V1ListDashboardsResponse listProjectDashboardNames(owner, project, offset, limit, sort, query)

List bookmarked runs for user

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
    V1ListDashboardsResponse result = apiInstance.listProjectDashboardNames(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#listProjectDashboardNames");
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

<a name="listProjectDashboards"></a>
# **listProjectDashboards**
> V1ListDashboardsResponse listProjectDashboards(owner, project, offset, limit, sort, query)

List archived runs for user

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
    V1ListDashboardsResponse result = apiInstance.listProjectDashboards(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#listProjectDashboards");
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

<a name="patchProjectDashboard"></a>
# **patchProjectDashboard**
> V1Dashboard patchProjectDashboard(owner, project, dashboardUuid, body)

Update run

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
    V1Dashboard result = apiInstance.patchProjectDashboard(owner, project, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#patchProjectDashboard");
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

<a name="promoteProjectDashboard"></a>
# **promoteProjectDashboard**
> V1Dashboard promoteProjectDashboard(owner, project, dashboardUuid)

Delete run

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
    V1Dashboard result = apiInstance.promoteProjectDashboard(owner, project, dashboardUuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#promoteProjectDashboard");
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

<a name="updateProjectDashboard"></a>
# **updateProjectDashboard**
> V1Dashboard updateProjectDashboard(owner, project, dashboardUuid, body)

Get run

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
    V1Dashboard result = apiInstance.updateProjectDashboard(owner, project, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectDashboardsV1Api#updateProjectDashboard");
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


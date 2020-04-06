# ProjectSearchesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projectSearchesV1CreateProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1CreateProjectSearch) | **POST** /api/v1/{owner}/{project}/searches | Create project search
[**projectSearchesV1DeleteProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1DeleteProjectSearch) | **DELETE** /api/v1/{owner}/{project}/searches/{uuid} | Delete project search
[**projectSearchesV1GetProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1GetProjectSearch) | **GET** /api/v1/{owner}/{project}/searches/{uuid} | Get project search
[**projectSearchesV1ListProjectSearchNames**](ProjectSearchesV1Api.md#projectSearchesV1ListProjectSearchNames) | **GET** /api/v1/{owner}/{project}/searches/names | List project search names
[**projectSearchesV1ListProjectSearches**](ProjectSearchesV1Api.md#projectSearchesV1ListProjectSearches) | **GET** /api/v1/{owner}/{project}/searches | List project searches
[**projectSearchesV1PatchProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1PatchProjectSearch) | **PATCH** /api/v1/{owner}/{project}/searches/{search.uuid} | Patch project search
[**projectSearchesV1PromoteProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1PromoteProjectSearch) | **POST** /api/v1/{owner}/{project}/searches/{uuid}/promote | Promote project search
[**projectSearchesV1UpdateProjectSearch**](ProjectSearchesV1Api.md#projectSearchesV1UpdateProjectSearch) | **PUT** /api/v1/{owner}/{project}/searches/{search.uuid} | Update project search


<a name="projectSearchesV1CreateProjectSearch"></a>
# **projectSearchesV1CreateProjectSearch**
> V1Search projectSearchesV1CreateProjectSearch(owner, project, body)

Create project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.projectSearchesV1CreateProjectSearch(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1CreateProjectSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectSearchesV1DeleteProjectSearch"></a>
# **projectSearchesV1DeleteProjectSearch**
> projectSearchesV1DeleteProjectSearch(owner, project, uuid)

Delete project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.projectSearchesV1DeleteProjectSearch(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1DeleteProjectSearch");
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

<a name="projectSearchesV1GetProjectSearch"></a>
# **projectSearchesV1GetProjectSearch**
> V1Search projectSearchesV1GetProjectSearch(owner, project, uuid)

Get project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Search result = apiInstance.projectSearchesV1GetProjectSearch(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1GetProjectSearch");
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

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectSearchesV1ListProjectSearchNames"></a>
# **projectSearchesV1ListProjectSearchNames**
> V1ListSearchesResponse projectSearchesV1ListProjectSearchNames(owner, project, offset, limit, sort, query)

List project search names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListSearchesResponse result = apiInstance.projectSearchesV1ListProjectSearchNames(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1ListProjectSearchNames");
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

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectSearchesV1ListProjectSearches"></a>
# **projectSearchesV1ListProjectSearches**
> V1ListSearchesResponse projectSearchesV1ListProjectSearches(owner, project, offset, limit, sort, query)

List project searches

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListSearchesResponse result = apiInstance.projectSearchesV1ListProjectSearches(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1ListProjectSearches");
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

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectSearchesV1PatchProjectSearch"></a>
# **projectSearchesV1PatchProjectSearch**
> V1Search projectSearchesV1PatchProjectSearch(owner, project, searchUuid, body)

Patch project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.projectSearchesV1PatchProjectSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1PatchProjectSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="projectSearchesV1PromoteProjectSearch"></a>
# **projectSearchesV1PromoteProjectSearch**
> projectSearchesV1PromoteProjectSearch(owner, project, uuid)

Promote project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.projectSearchesV1PromoteProjectSearch(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1PromoteProjectSearch");
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

<a name="projectSearchesV1UpdateProjectSearch"></a>
# **projectSearchesV1UpdateProjectSearch**
> V1Search projectSearchesV1UpdateProjectSearch(owner, project, searchUuid, body)

Update project search

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ProjectSearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ProjectSearchesV1Api apiInstance = new ProjectSearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.projectSearchesV1UpdateProjectSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#projectSearchesV1UpdateProjectSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


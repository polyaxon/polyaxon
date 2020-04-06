# ProjectSearchesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createProjectSearch**](ProjectSearchesV1Api.md#createProjectSearch) | **POST** /api/v1/{owner}/{project}/searches | Create project search
[**deleteProjectSearch**](ProjectSearchesV1Api.md#deleteProjectSearch) | **DELETE** /api/v1/{owner}/{project}/searches/{uuid} | Delete project search
[**getProjectSearch**](ProjectSearchesV1Api.md#getProjectSearch) | **GET** /api/v1/{owner}/{project}/searches/{uuid} | Get project search
[**listProjectSearchNames**](ProjectSearchesV1Api.md#listProjectSearchNames) | **GET** /api/v1/{owner}/{project}/searches/names | List project search names
[**listProjectSearches**](ProjectSearchesV1Api.md#listProjectSearches) | **GET** /api/v1/{owner}/{project}/searches | List project searches
[**patchProjectSearch**](ProjectSearchesV1Api.md#patchProjectSearch) | **PATCH** /api/v1/{owner}/{project}/searches/{search.uuid} | Patch project search
[**promoteProjectSearch**](ProjectSearchesV1Api.md#promoteProjectSearch) | **POST** /api/v1/{owner}/{project}/searches/{uuid}/promote | Promote project search
[**updateProjectSearch**](ProjectSearchesV1Api.md#updateProjectSearch) | **PUT** /api/v1/{owner}/{project}/searches/{search.uuid} | Update project search


<a name="createProjectSearch"></a>
# **createProjectSearch**
> V1Search createProjectSearch(owner, project, body)

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
    V1Search result = apiInstance.createProjectSearch(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#createProjectSearch");
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

<a name="deleteProjectSearch"></a>
# **deleteProjectSearch**
> deleteProjectSearch(owner, project, uuid)

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
    apiInstance.deleteProjectSearch(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#deleteProjectSearch");
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

<a name="getProjectSearch"></a>
# **getProjectSearch**
> V1Search getProjectSearch(owner, project, uuid)

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
    V1Search result = apiInstance.getProjectSearch(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#getProjectSearch");
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

<a name="listProjectSearchNames"></a>
# **listProjectSearchNames**
> V1ListSearchesResponse listProjectSearchNames(owner, project, offset, limit, sort, query)

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
    V1ListSearchesResponse result = apiInstance.listProjectSearchNames(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#listProjectSearchNames");
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

<a name="listProjectSearches"></a>
# **listProjectSearches**
> V1ListSearchesResponse listProjectSearches(owner, project, offset, limit, sort, query)

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
    V1ListSearchesResponse result = apiInstance.listProjectSearches(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#listProjectSearches");
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

<a name="patchProjectSearch"></a>
# **patchProjectSearch**
> V1Search patchProjectSearch(owner, project, searchUuid, body)

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
    V1Search result = apiInstance.patchProjectSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#patchProjectSearch");
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

<a name="promoteProjectSearch"></a>
# **promoteProjectSearch**
> promoteProjectSearch(owner, project, uuid)

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
    apiInstance.promoteProjectSearch(owner, project, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#promoteProjectSearch");
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

<a name="updateProjectSearch"></a>
# **updateProjectSearch**
> V1Search updateProjectSearch(owner, project, searchUuid, body)

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
    V1Search result = apiInstance.updateProjectSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ProjectSearchesV1Api#updateProjectSearch");
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


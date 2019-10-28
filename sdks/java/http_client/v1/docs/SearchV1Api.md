# SearchV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createSearch**](SearchV1Api.md#createSearch) | **POST** /api/v1/{owner}/{project}/searches | List archived runs for user
[**deleteSearch**](SearchV1Api.md#deleteSearch) | **DELETE** /api/v1/{owner}/{project}/searches/{uuid} | Update run
[**getSearch**](SearchV1Api.md#getSearch) | **GET** /api/v1/{owner}/{project}/searches/{uuid} | List runs
[**listSearches**](SearchV1Api.md#listSearches) | **GET** /api/v1/{owner}/{project}/searches | List bookmarked runs for user
[**patchSearch**](SearchV1Api.md#patchSearch) | **PATCH** /api/v1/{owner}/{project}/searches/{search.uuid} | Get run
[**updateSearch**](SearchV1Api.md#updateSearch) | **PUT** /api/v1/{owner}/{project}/searches/{search.uuid} | Create new run


<a name="createSearch"></a>
# **createSearch**
> V1Search createSearch(owner, project, body)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
V1Search body = new V1Search(); // V1Search | Artifact store body
try {
    V1Search result = apiInstance.createSearch(owner, project, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#createSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **body** | [**V1Search**](V1Search.md)| Artifact store body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteSearch"></a>
# **deleteSearch**
> Object deleteSearch(owner, project, uuid)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteSearch(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#deleteSearch");
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

<a name="getSearch"></a>
# **getSearch**
> V1Search getSearch(owner, project, uuid)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project where the experiement will be assigned
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Search result = apiInstance.getSearch(owner, project, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#getSearch");
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

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listSearches"></a>
# **listSearches**
> V1ListSearchesResponse listSearches(owner, project, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListSearchesResponse result = apiInstance.listSearches(owner, project, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#listSearches");
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

<a name="patchSearch"></a>
# **patchSearch**
> V1Search patchSearch(owner, project, searchUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Artifact store body
try {
    V1Search result = apiInstance.patchSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#patchSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Artifact store body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateSearch"></a>
# **updateSearch**
> V1Search updateSearch(owner, project, searchUuid, body)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchV1Api apiInstance = new SearchV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String project = "project_example"; // String | Project under namesapce
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Artifact store body
try {
    V1Search result = apiInstance.updateSearch(owner, project, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchV1Api#updateSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **project** | **String**| Project under namesapce |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Artifact store body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


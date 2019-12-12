# SearchesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createSearch**](SearchesV1Api.md#createSearch) | **POST** /api/v1/orgs/{owner}/searches | List runs
[**deleteSearch**](SearchesV1Api.md#deleteSearch) | **DELETE** /api/v1/orgs/{owner}/searches/{uuid} | Patch run
[**getSearch**](SearchesV1Api.md#getSearch) | **GET** /api/v1/orgs/{owner}/searches/{uuid} | Create new run
[**listSearchNames**](SearchesV1Api.md#listSearchNames) | **GET** /api/v1/orgs/{owner}/searches/names | List bookmarked runs for user
[**listSearches**](SearchesV1Api.md#listSearches) | **GET** /api/v1/orgs/{owner}/searches | List archived runs for user
[**patchSearch**](SearchesV1Api.md#patchSearch) | **PATCH** /api/v1/orgs/{owner}/searches/{search.uuid} | Update run
[**updateSearch**](SearchesV1Api.md#updateSearch) | **PUT** /api/v1/orgs/{owner}/searches/{search.uuid} | Get run


<a name="createSearch"></a>
# **createSearch**
> V1Search createSearch(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.createSearch(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#createSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteSearch"></a>
# **deleteSearch**
> deleteSearch(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteSearch(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#deleteSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getSearch"></a>
# **getSearch**
> V1Search getSearch(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1Search result = apiInstance.getSearch(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#getSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listSearchNames"></a>
# **listSearchNames**
> V1ListSearchesResponse listSearchNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListSearchesResponse result = apiInstance.listSearchNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#listSearchNames");
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

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listSearches"></a>
# **listSearches**
> V1ListSearchesResponse listSearches(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListSearchesResponse result = apiInstance.listSearches(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#listSearches");
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

[**V1ListSearchesResponse**](V1ListSearchesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchSearch"></a>
# **patchSearch**
> V1Search patchSearch(owner, searchUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.patchSearch(owner, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#patchSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateSearch"></a>
# **updateSearch**
> V1Search updateSearch(owner, searchUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.SearchesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

SearchesV1Api apiInstance = new SearchesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String searchUuid = "searchUuid_example"; // String | UUID
V1Search body = new V1Search(); // V1Search | Search body
try {
    V1Search result = apiInstance.updateSearch(owner, searchUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling SearchesV1Api#updateSearch");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **searchUuid** | **String**| UUID |
 **body** | [**V1Search**](V1Search.md)| Search body |

### Return type

[**V1Search**](V1Search.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


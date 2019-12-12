# GitAccessesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createGitAccess**](GitAccessesV1Api.md#createGitAccess) | **POST** /api/v1/orgs/{owner}/git_accesses | List runs
[**deleteGitAccess**](GitAccessesV1Api.md#deleteGitAccess) | **DELETE** /api/v1/orgs/{owner}/git_accesses/{uuid} | Patch run
[**getGitAccess**](GitAccessesV1Api.md#getGitAccess) | **GET** /api/v1/orgs/{owner}/git_accesses/{uuid} | Create new run
[**listGitAccessNames**](GitAccessesV1Api.md#listGitAccessNames) | **GET** /api/v1/orgs/{owner}/git_accesses/names | List bookmarked runs for user
[**listGitAccesses**](GitAccessesV1Api.md#listGitAccesses) | **GET** /api/v1/orgs/{owner}/git_accesses | List archived runs for user
[**patchGitAccess**](GitAccessesV1Api.md#patchGitAccess) | **PATCH** /api/v1/orgs/{owner}/git_accesses/{host_access.uuid} | Update run
[**updateGitAccess**](GitAccessesV1Api.md#updateGitAccess) | **PUT** /api/v1/orgs/{owner}/git_accesses/{host_access.uuid} | Get run


<a name="createGitAccess"></a>
# **createGitAccess**
> V1HostAccess createGitAccess(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.createGitAccess(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#createGitAccess");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1HostAccess**](V1HostAccess.md)| Artifact store body |

### Return type

[**V1HostAccess**](V1HostAccess.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteGitAccess"></a>
# **deleteGitAccess**
> deleteGitAccess(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteGitAccess(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#deleteGitAccess");
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

<a name="getGitAccess"></a>
# **getGitAccess**
> V1HostAccess getGitAccess(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1HostAccess result = apiInstance.getGitAccess(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#getGitAccess");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1HostAccess**](V1HostAccess.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listGitAccessNames"></a>
# **listGitAccessNames**
> V1ListHostAccessesResponse listGitAccessNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listGitAccessNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#listGitAccessNames");
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

[**V1ListHostAccessesResponse**](V1ListHostAccessesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listGitAccesses"></a>
# **listGitAccesses**
> V1ListHostAccessesResponse listGitAccesses(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listGitAccesses(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#listGitAccesses");
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

[**V1ListHostAccessesResponse**](V1ListHostAccessesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchGitAccess"></a>
# **patchGitAccess**
> V1HostAccess patchGitAccess(owner, hostAccessUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.patchGitAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#patchGitAccess");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **hostAccessUuid** | **String**| UUID |
 **body** | [**V1HostAccess**](V1HostAccess.md)| Artifact store body |

### Return type

[**V1HostAccess**](V1HostAccess.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateGitAccess"></a>
# **updateGitAccess**
> V1HostAccess updateGitAccess(owner, hostAccessUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.GitAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

GitAccessesV1Api apiInstance = new GitAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.updateGitAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling GitAccessesV1Api#updateGitAccess");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **hostAccessUuid** | **String**| UUID |
 **body** | [**V1HostAccess**](V1HostAccess.md)| Artifact store body |

### Return type

[**V1HostAccess**](V1HostAccess.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


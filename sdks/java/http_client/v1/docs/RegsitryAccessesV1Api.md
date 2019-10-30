# RegsitryAccessesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createRegsitryAccess**](RegsitryAccessesV1Api.md#createRegsitryAccess) | **POST** /api/v1/{owner}/registry_accesses | List runs
[**deleteRegsitryAccess**](RegsitryAccessesV1Api.md#deleteRegsitryAccess) | **DELETE** /api/v1/{owner}/registry_accesses/{uuid} | Patch run
[**getRegsitryAccess**](RegsitryAccessesV1Api.md#getRegsitryAccess) | **GET** /api/v1/{owner}/registry_accesses/{uuid} | Create new run
[**listRegsitryAccessNames**](RegsitryAccessesV1Api.md#listRegsitryAccessNames) | **GET** /api/v1/{owner}/registry_accesses/names | List bookmarked runs for user
[**listRegsitryAccesses**](RegsitryAccessesV1Api.md#listRegsitryAccesses) | **GET** /api/v1/{owner}/registry_accesses | List archived runs for user
[**patchRegsitryAccess**](RegsitryAccessesV1Api.md#patchRegsitryAccess) | **PATCH** /api/v1/{owner}/registry_accesses/{host_access.uuid} | Update run
[**updateRegsitryAccess**](RegsitryAccessesV1Api.md#updateRegsitryAccess) | **PUT** /api/v1/{owner}/registry_accesses/{host_access.uuid} | Get run


<a name="createRegsitryAccess"></a>
# **createRegsitryAccess**
> V1HostAccess createRegsitryAccess(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.createRegsitryAccess(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#createRegsitryAccess");
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

<a name="deleteRegsitryAccess"></a>
# **deleteRegsitryAccess**
> deleteRegsitryAccess(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteRegsitryAccess(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#deleteRegsitryAccess");
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

<a name="getRegsitryAccess"></a>
# **getRegsitryAccess**
> V1HostAccess getRegsitryAccess(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1HostAccess result = apiInstance.getRegsitryAccess(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#getRegsitryAccess");
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

<a name="listRegsitryAccessNames"></a>
# **listRegsitryAccessNames**
> V1ListHostAccessesResponse listRegsitryAccessNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listRegsitryAccessNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#listRegsitryAccessNames");
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

<a name="listRegsitryAccesses"></a>
# **listRegsitryAccesses**
> V1ListHostAccessesResponse listRegsitryAccesses(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listRegsitryAccesses(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#listRegsitryAccesses");
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

<a name="patchRegsitryAccess"></a>
# **patchRegsitryAccess**
> V1HostAccess patchRegsitryAccess(owner, hostAccessUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.patchRegsitryAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#patchRegsitryAccess");
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

<a name="updateRegsitryAccess"></a>
# **updateRegsitryAccess**
> V1HostAccess updateRegsitryAccess(owner, hostAccessUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegsitryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegsitryAccessesV1Api apiInstance = new RegsitryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.updateRegsitryAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegsitryAccessesV1Api#updateRegsitryAccess");
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


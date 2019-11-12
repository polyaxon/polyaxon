# RegistryAccessesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createRegistryAccess**](RegistryAccessesV1Api.md#createRegistryAccess) | **POST** /api/v1/{owner}/registry_accesses | List runs
[**deleteRegistryAccess**](RegistryAccessesV1Api.md#deleteRegistryAccess) | **DELETE** /api/v1/{owner}/registry_accesses/{uuid} | Patch run
[**getRegistryAccess**](RegistryAccessesV1Api.md#getRegistryAccess) | **GET** /api/v1/{owner}/registry_accesses/{uuid} | Create new run
[**listRegistryAccessNames**](RegistryAccessesV1Api.md#listRegistryAccessNames) | **GET** /api/v1/{owner}/registry_accesses/names | List bookmarked runs for user
[**listRegistryAccesses**](RegistryAccessesV1Api.md#listRegistryAccesses) | **GET** /api/v1/{owner}/registry_accesses | List archived runs for user
[**patchRegistryAccess**](RegistryAccessesV1Api.md#patchRegistryAccess) | **PATCH** /api/v1/{owner}/registry_accesses/{host_access.uuid} | Update run
[**updateRegistryAccess**](RegistryAccessesV1Api.md#updateRegistryAccess) | **PUT** /api/v1/{owner}/registry_accesses/{host_access.uuid} | Get run


<a name="createRegistryAccess"></a>
# **createRegistryAccess**
> V1HostAccess createRegistryAccess(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.createRegistryAccess(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#createRegistryAccess");
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

<a name="deleteRegistryAccess"></a>
# **deleteRegistryAccess**
> deleteRegistryAccess(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteRegistryAccess(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#deleteRegistryAccess");
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

<a name="getRegistryAccess"></a>
# **getRegistryAccess**
> V1HostAccess getRegistryAccess(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1HostAccess result = apiInstance.getRegistryAccess(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#getRegistryAccess");
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

<a name="listRegistryAccessNames"></a>
# **listRegistryAccessNames**
> V1ListHostAccessesResponse listRegistryAccessNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listRegistryAccessNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#listRegistryAccessNames");
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

<a name="listRegistryAccesses"></a>
# **listRegistryAccesses**
> V1ListHostAccessesResponse listRegistryAccesses(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHostAccessesResponse result = apiInstance.listRegistryAccesses(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#listRegistryAccesses");
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

<a name="patchRegistryAccess"></a>
# **patchRegistryAccess**
> V1HostAccess patchRegistryAccess(owner, hostAccessUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.patchRegistryAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#patchRegistryAccess");
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

<a name="updateRegistryAccess"></a>
# **updateRegistryAccess**
> V1HostAccess updateRegistryAccess(owner, hostAccessUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RegistryAccessesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RegistryAccessesV1Api apiInstance = new RegistryAccessesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String hostAccessUuid = "hostAccessUuid_example"; // String | UUID
V1HostAccess body = new V1HostAccess(); // V1HostAccess | Artifact store body
try {
    V1HostAccess result = apiInstance.updateRegistryAccess(owner, hostAccessUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RegistryAccessesV1Api#updateRegistryAccess");
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


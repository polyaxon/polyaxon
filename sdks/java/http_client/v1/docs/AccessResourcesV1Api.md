# AccessResourcesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accessResourcesV1CreateAccessResource**](AccessResourcesV1Api.md#accessResourcesV1CreateAccessResource) | **POST** /api/v1/orgs/{owner}/access_resources | Create access resource
[**accessResourcesV1DeleteAccessResource**](AccessResourcesV1Api.md#accessResourcesV1DeleteAccessResource) | **DELETE** /api/v1/orgs/{owner}/access_resources/{uuid} | Delete access resource
[**accessResourcesV1GetAccessResource**](AccessResourcesV1Api.md#accessResourcesV1GetAccessResource) | **GET** /api/v1/orgs/{owner}/access_resources/{uuid} | Get access resource
[**accessResourcesV1ListAccessResourceNames**](AccessResourcesV1Api.md#accessResourcesV1ListAccessResourceNames) | **GET** /api/v1/orgs/{owner}/access_resources/names | List access resource names
[**accessResourcesV1ListAccessResources**](AccessResourcesV1Api.md#accessResourcesV1ListAccessResources) | **GET** /api/v1/orgs/{owner}/access_resources | List access resources
[**accessResourcesV1PatchAccessResource**](AccessResourcesV1Api.md#accessResourcesV1PatchAccessResource) | **PATCH** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Patch access resource
[**accessResourcesV1UpdateAccessResource**](AccessResourcesV1Api.md#accessResourcesV1UpdateAccessResource) | **PUT** /api/v1/orgs/{owner}/access_resources/{access_resource.uuid} | Update access resource


<a name="accessResourcesV1CreateAccessResource"></a>
# **accessResourcesV1CreateAccessResource**
> V1AccessResource accessResourcesV1CreateAccessResource(owner, body)

Create access resource

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
try {
    V1AccessResource result = apiInstance.accessResourcesV1CreateAccessResource(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1CreateAccessResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1DeleteAccessResource"></a>
# **accessResourcesV1DeleteAccessResource**
> accessResourcesV1DeleteAccessResource(owner, uuid)

Delete access resource

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.accessResourcesV1DeleteAccessResource(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1DeleteAccessResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1GetAccessResource"></a>
# **accessResourcesV1GetAccessResource**
> V1AccessResource accessResourcesV1GetAccessResource(owner, uuid)

Get access resource

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1AccessResource result = apiInstance.accessResourcesV1GetAccessResource(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1GetAccessResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1ListAccessResourceNames"></a>
# **accessResourcesV1ListAccessResourceNames**
> V1ListAccessResourcesResponse accessResourcesV1ListAccessResourceNames(owner, offset, limit, sort, query)

List access resource names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListAccessResourcesResponse result = apiInstance.accessResourcesV1ListAccessResourceNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1ListAccessResourceNames");
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

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1ListAccessResources"></a>
# **accessResourcesV1ListAccessResources**
> V1ListAccessResourcesResponse accessResourcesV1ListAccessResources(owner, offset, limit, sort, query)

List access resources

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListAccessResourcesResponse result = apiInstance.accessResourcesV1ListAccessResources(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1ListAccessResources");
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

[**V1ListAccessResourcesResponse**](V1ListAccessResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1PatchAccessResource"></a>
# **accessResourcesV1PatchAccessResource**
> V1AccessResource accessResourcesV1PatchAccessResource(owner, accessResourceUuid, body)

Patch access resource

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String accessResourceUuid = "accessResourceUuid_example"; // String | UUID
V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
try {
    V1AccessResource result = apiInstance.accessResourcesV1PatchAccessResource(owner, accessResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1PatchAccessResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **accessResourceUuid** | **String**| UUID |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="accessResourcesV1UpdateAccessResource"></a>
# **accessResourcesV1UpdateAccessResource**
> V1AccessResource accessResourcesV1UpdateAccessResource(owner, accessResourceUuid, body)

Update access resource

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AccessResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AccessResourcesV1Api apiInstance = new AccessResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String accessResourceUuid = "accessResourceUuid_example"; // String | UUID
V1AccessResource body = new V1AccessResource(); // V1AccessResource | Artifact store body
try {
    V1AccessResource result = apiInstance.accessResourcesV1UpdateAccessResource(owner, accessResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AccessResourcesV1Api#accessResourcesV1UpdateAccessResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **accessResourceUuid** | **String**| UUID |
 **body** | [**V1AccessResource**](V1AccessResource.md)| Artifact store body |

### Return type

[**V1AccessResource**](V1AccessResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


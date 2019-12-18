# ConfigResourcesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createConfigResource**](ConfigResourcesV1Api.md#createConfigResource) | **POST** /api/v1/orgs/{owner}/config_resources | List runs
[**deleteConfigResource**](ConfigResourcesV1Api.md#deleteConfigResource) | **DELETE** /api/v1/orgs/{owner}/config_resources/{uuid} | Patch run
[**getConfigResource**](ConfigResourcesV1Api.md#getConfigResource) | **GET** /api/v1/orgs/{owner}/config_resources/{uuid} | Create new run
[**listConfigResourceNames**](ConfigResourcesV1Api.md#listConfigResourceNames) | **GET** /api/v1/orgs/{owner}/config_resources/names | List bookmarked runs for user
[**listConfigResources**](ConfigResourcesV1Api.md#listConfigResources) | **GET** /api/v1/orgs/{owner}/config_resources | List archived runs for user
[**patchConfigResource**](ConfigResourcesV1Api.md#patchConfigResource) | **PATCH** /api/v1/orgs/{owner}/config_resources/{config_resource.uuid} | Update run
[**updateConfigResource**](ConfigResourcesV1Api.md#updateConfigResource) | **PUT** /api/v1/orgs/{owner}/config_resources/{config_resource.uuid} | Get run


<a name="createConfigResource"></a>
# **createConfigResource**
> V1ConfigResource createConfigResource(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1ConfigResource body = new V1ConfigResource(); // V1ConfigResource | Artifact store body
try {
    V1ConfigResource result = apiInstance.createConfigResource(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#createConfigResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1ConfigResource**](V1ConfigResource.md)| Artifact store body |

### Return type

[**V1ConfigResource**](V1ConfigResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteConfigResource"></a>
# **deleteConfigResource**
> deleteConfigResource(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteConfigResource(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#deleteConfigResource");
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

<a name="getConfigResource"></a>
# **getConfigResource**
> V1ConfigResource getConfigResource(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1ConfigResource result = apiInstance.getConfigResource(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#getConfigResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1ConfigResource**](V1ConfigResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listConfigResourceNames"></a>
# **listConfigResourceNames**
> V1ListConfigResourcesResponse listConfigResourceNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConfigResourcesResponse result = apiInstance.listConfigResourceNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#listConfigResourceNames");
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

[**V1ListConfigResourcesResponse**](V1ListConfigResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listConfigResources"></a>
# **listConfigResources**
> V1ListConfigResourcesResponse listConfigResources(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListConfigResourcesResponse result = apiInstance.listConfigResources(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#listConfigResources");
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

[**V1ListConfigResourcesResponse**](V1ListConfigResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchConfigResource"></a>
# **patchConfigResource**
> V1ConfigResource patchConfigResource(owner, configResourceUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String configResourceUuid = "configResourceUuid_example"; // String | UUID
V1ConfigResource body = new V1ConfigResource(); // V1ConfigResource | Artifact store body
try {
    V1ConfigResource result = apiInstance.patchConfigResource(owner, configResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#patchConfigResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **configResourceUuid** | **String**| UUID |
 **body** | [**V1ConfigResource**](V1ConfigResource.md)| Artifact store body |

### Return type

[**V1ConfigResource**](V1ConfigResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateConfigResource"></a>
# **updateConfigResource**
> V1ConfigResource updateConfigResource(owner, configResourceUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.ConfigResourcesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

ConfigResourcesV1Api apiInstance = new ConfigResourcesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String configResourceUuid = "configResourceUuid_example"; // String | UUID
V1ConfigResource body = new V1ConfigResource(); // V1ConfigResource | Artifact store body
try {
    V1ConfigResource result = apiInstance.updateConfigResource(owner, configResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling ConfigResourcesV1Api#updateConfigResource");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **configResourceUuid** | **String**| UUID |
 **body** | [**V1ConfigResource**](V1ConfigResource.md)| Artifact store body |

### Return type

[**V1ConfigResource**](V1ConfigResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


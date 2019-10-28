# K8SConfigMapsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8SConfigMaps**](K8SConfigMapsV1Api.md#createK8SConfigMaps) | **POST** /api/v1/{owner}/k8s_config_maps | List runs
[**deleteK8SConfigMap**](K8SConfigMapsV1Api.md#deleteK8SConfigMap) | **DELETE** /api/v1/{owner}/k8s_config_maps/{uuid} | Patch run
[**getK8SConfigMap**](K8SConfigMapsV1Api.md#getK8SConfigMap) | **GET** /api/v1/{owner}/k8s_config_maps/{uuid} | Create new run
[**listK8SConfigMapNames**](K8SConfigMapsV1Api.md#listK8SConfigMapNames) | **GET** /api/v1/{owner}/k8s_config_maps/names | List bookmarked runs for user
[**listK8SConfigMaps**](K8SConfigMapsV1Api.md#listK8SConfigMaps) | **GET** /api/v1/{owner}/k8s_config_maps | List archived runs for user
[**patchK8SConfigMap**](K8SConfigMapsV1Api.md#patchK8SConfigMap) | **PATCH** /api/v1/{owner}/k8s_config_maps/{k8s_resource.uuid} | Update run
[**updateK8SConfigMap**](K8SConfigMapsV1Api.md#updateK8SConfigMap) | **PUT** /api/v1/{owner}/k8s_config_maps/{k8s_resource.uuid} | Get run


<a name="createK8SConfigMaps"></a>
# **createK8SConfigMaps**
> V1K8SResource createK8SConfigMaps(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.createK8SConfigMaps(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#createK8SConfigMaps");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8SConfigMap"></a>
# **deleteK8SConfigMap**
> Object deleteK8SConfigMap(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    Object result = apiInstance.deleteK8SConfigMap(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#deleteK8SConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getK8SConfigMap"></a>
# **getK8SConfigMap**
> V1K8SResource getK8SConfigMap(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1K8SResource result = apiInstance.getK8SConfigMap(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#getK8SConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SConfigMapNames"></a>
# **listK8SConfigMapNames**
> V1ListK8SResourcesResponse listK8SConfigMapNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8SResourcesResponse result = apiInstance.listK8SConfigMapNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#listK8SConfigMapNames");
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8SConfigMaps"></a>
# **listK8SConfigMaps**
> V1ListK8SResourcesResponse listK8SConfigMaps(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8SResourcesResponse result = apiInstance.listK8SConfigMaps(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#listK8SConfigMaps");
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

[**V1ListK8SResourcesResponse**](V1ListK8SResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8SConfigMap"></a>
# **patchK8SConfigMap**
> V1K8SResource patchK8SConfigMap(owner, k8sResourceUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.patchK8SConfigMap(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#patchK8SConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8SConfigMap"></a>
# **updateK8SConfigMap**
> V1K8SResource updateK8SConfigMap(owner, k8sResourceUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8SConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8SConfigMapsV1Api apiInstance = new K8SConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8SResource body = new V1K8SResource(); // V1K8SResource | Artifact store body
try {
    V1K8SResource result = apiInstance.updateK8SConfigMap(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8SConfigMapsV1Api#updateK8SConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8SResource**](V1K8SResource.md)| Artifact store body |

### Return type

[**V1K8SResource**](V1K8SResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


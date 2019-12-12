# K8sConfigMapsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createK8sConfigMap**](K8sConfigMapsV1Api.md#createK8sConfigMap) | **POST** /api/v1/orgs/{owner}/k8s_config_maps | List runs
[**deleteK8sConfigMap**](K8sConfigMapsV1Api.md#deleteK8sConfigMap) | **DELETE** /api/v1/orgs/{owner}/k8s_config_maps/{uuid} | Patch run
[**getK8sConfigMap**](K8sConfigMapsV1Api.md#getK8sConfigMap) | **GET** /api/v1/orgs/{owner}/k8s_config_maps/{uuid} | Create new run
[**listK8sConfigMapNames**](K8sConfigMapsV1Api.md#listK8sConfigMapNames) | **GET** /api/v1/orgs/{owner}/k8s_config_maps/names | List bookmarked runs for user
[**listK8sConfigMaps**](K8sConfigMapsV1Api.md#listK8sConfigMaps) | **GET** /api/v1/orgs/{owner}/k8s_config_maps | List archived runs for user
[**patchK8sConfigMap**](K8sConfigMapsV1Api.md#patchK8sConfigMap) | **PATCH** /api/v1/orgs/{owner}/k8s_config_maps/{k8s_resource.uuid} | Update run
[**updateK8sConfigMap**](K8sConfigMapsV1Api.md#updateK8sConfigMap) | **PUT** /api/v1/orgs/{owner}/k8s_config_maps/{k8s_resource.uuid} | Get run


<a name="createK8sConfigMap"></a>
# **createK8sConfigMap**
> V1K8sResource createK8sConfigMap(owner, body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.createK8sConfigMap(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#createK8sConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteK8sConfigMap"></a>
# **deleteK8sConfigMap**
> deleteK8sConfigMap(owner, uuid)

Patch run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    apiInstance.deleteK8sConfigMap(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#deleteK8sConfigMap");
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

<a name="getK8sConfigMap"></a>
# **getK8sConfigMap**
> V1K8sResource getK8sConfigMap(owner, uuid)

Create new run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Unique integer identifier of the entity
try {
    V1K8sResource result = apiInstance.getK8sConfigMap(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#getK8sConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Unique integer identifier of the entity |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sConfigMapNames"></a>
# **listK8sConfigMapNames**
> V1ListK8sResourcesResponse listK8sConfigMapNames(owner, offset, limit, sort, query)

List bookmarked runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8sResourcesResponse result = apiInstance.listK8sConfigMapNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#listK8sConfigMapNames");
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listK8sConfigMaps"></a>
# **listK8sConfigMaps**
> V1ListK8sResourcesResponse listK8sConfigMaps(owner, offset, limit, sort, query)

List archived runs for user

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListK8sResourcesResponse result = apiInstance.listK8sConfigMaps(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#listK8sConfigMaps");
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

[**V1ListK8sResourcesResponse**](V1ListK8sResourcesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchK8sConfigMap"></a>
# **patchK8sConfigMap**
> V1K8sResource patchK8sConfigMap(owner, k8sResourceUuid, body)

Update run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.patchK8sConfigMap(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#patchK8sConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateK8sConfigMap"></a>
# **updateK8sConfigMap**
> V1K8sResource updateK8sConfigMap(owner, k8sResourceUuid, body)

Get run

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.K8sConfigMapsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

K8sConfigMapsV1Api apiInstance = new K8sConfigMapsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String k8sResourceUuid = "k8sResourceUuid_example"; // String | UUID
V1K8sResource body = new V1K8sResource(); // V1K8sResource | Artifact store body
try {
    V1K8sResource result = apiInstance.updateK8sConfigMap(owner, k8sResourceUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling K8sConfigMapsV1Api#updateK8sConfigMap");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **k8sResourceUuid** | **String**| UUID |
 **body** | [**V1K8sResource**](V1K8sResource.md)| Artifact store body |

### Return type

[**V1K8sResource**](V1K8sResource.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


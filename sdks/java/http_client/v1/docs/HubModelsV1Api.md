# HubModelsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createHubModel**](HubModelsV1Api.md#createHubModel) | **POST** /api/v1/orgs/{owner}/models | Create dashboard
[**deleteHubModel**](HubModelsV1Api.md#deleteHubModel) | **DELETE** /api/v1/orgs/{owner}/models/{uuid} | Delete dashboard
[**getHubModel**](HubModelsV1Api.md#getHubModel) | **GET** /api/v1/orgs/{owner}/models/{uuid} | Get dashboard
[**listHubModelNames**](HubModelsV1Api.md#listHubModelNames) | **GET** /api/v1/orgs/{owner}/models/names | List dashboard names
[**listHubModels**](HubModelsV1Api.md#listHubModels) | **GET** /api/v1/orgs/{owner}/models | List dashboards
[**patchHubModel**](HubModelsV1Api.md#patchHubModel) | **PATCH** /api/v1/orgs/{owner}/models/{model.uuid} | Patch dashboard
[**updateHubModel**](HubModelsV1Api.md#updateHubModel) | **PUT** /api/v1/orgs/{owner}/models/{model.uuid} | Update dashboard


<a name="createHubModel"></a>
# **createHubModel**
> V1HubModel createHubModel(owner, body)

Create dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1HubModel body = new V1HubModel(); // V1HubModel | Model body
try {
    V1HubModel result = apiInstance.createHubModel(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#createHubModel");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1HubModel**](V1HubModel.md)| Model body |

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteHubModel"></a>
# **deleteHubModel**
> deleteHubModel(owner, uuid)

Delete dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.deleteHubModel(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#deleteHubModel");
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

<a name="getHubModel"></a>
# **getHubModel**
> V1HubModel getHubModel(owner, uuid)

Get dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1HubModel result = apiInstance.getHubModel(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#getHubModel");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listHubModelNames"></a>
# **listHubModelNames**
> V1ListHubModelsResponse listHubModelNames(owner, offset, limit, sort, query)

List dashboard names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHubModelsResponse result = apiInstance.listHubModelNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#listHubModelNames");
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

[**V1ListHubModelsResponse**](V1ListHubModelsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listHubModels"></a>
# **listHubModels**
> V1ListHubModelsResponse listHubModels(owner, offset, limit, sort, query)

List dashboards

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListHubModelsResponse result = apiInstance.listHubModels(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#listHubModels");
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

[**V1ListHubModelsResponse**](V1ListHubModelsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchHubModel"></a>
# **patchHubModel**
> V1HubModel patchHubModel(owner, modelUuid, body)

Patch dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String modelUuid = "modelUuid_example"; // String | UUID
V1HubModel body = new V1HubModel(); // V1HubModel | Model body
try {
    V1HubModel result = apiInstance.patchHubModel(owner, modelUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#patchHubModel");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **modelUuid** | **String**| UUID |
 **body** | [**V1HubModel**](V1HubModel.md)| Model body |

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateHubModel"></a>
# **updateHubModel**
> V1HubModel updateHubModel(owner, modelUuid, body)

Update dashboard

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.HubModelsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

HubModelsV1Api apiInstance = new HubModelsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String modelUuid = "modelUuid_example"; // String | UUID
V1HubModel body = new V1HubModel(); // V1HubModel | Model body
try {
    V1HubModel result = apiInstance.updateHubModel(owner, modelUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#updateHubModel");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **modelUuid** | **String**| UUID |
 **body** | [**V1HubModel**](V1HubModel.md)| Model body |

### Return type

[**V1HubModel**](V1HubModel.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


# HubModelsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**hubModelsV1CreateHubModel**](HubModelsV1Api.md#hubModelsV1CreateHubModel) | **POST** /api/v1/orgs/{owner}/models | Create dashboard
[**hubModelsV1DeleteHubModel**](HubModelsV1Api.md#hubModelsV1DeleteHubModel) | **DELETE** /api/v1/orgs/{owner}/models/{uuid} | Delete dashboard
[**hubModelsV1GetHubModel**](HubModelsV1Api.md#hubModelsV1GetHubModel) | **GET** /api/v1/orgs/{owner}/models/{uuid} | Get dashboard
[**hubModelsV1ListHubModelNames**](HubModelsV1Api.md#hubModelsV1ListHubModelNames) | **GET** /api/v1/orgs/{owner}/models/names | List dashboard names
[**hubModelsV1ListHubModels**](HubModelsV1Api.md#hubModelsV1ListHubModels) | **GET** /api/v1/orgs/{owner}/models | List dashboards
[**hubModelsV1PatchHubModel**](HubModelsV1Api.md#hubModelsV1PatchHubModel) | **PATCH** /api/v1/orgs/{owner}/models/{model.uuid} | Patch dashboard
[**hubModelsV1UpdateHubModel**](HubModelsV1Api.md#hubModelsV1UpdateHubModel) | **PUT** /api/v1/orgs/{owner}/models/{model.uuid} | Update dashboard


<a name="hubModelsV1CreateHubModel"></a>
# **hubModelsV1CreateHubModel**
> V1HubModel hubModelsV1CreateHubModel(owner, body)

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
    V1HubModel result = apiInstance.hubModelsV1CreateHubModel(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1CreateHubModel");
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

<a name="hubModelsV1DeleteHubModel"></a>
# **hubModelsV1DeleteHubModel**
> hubModelsV1DeleteHubModel(owner, uuid)

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
    apiInstance.hubModelsV1DeleteHubModel(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1DeleteHubModel");
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

<a name="hubModelsV1GetHubModel"></a>
# **hubModelsV1GetHubModel**
> V1HubModel hubModelsV1GetHubModel(owner, uuid)

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
    V1HubModel result = apiInstance.hubModelsV1GetHubModel(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1GetHubModel");
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

<a name="hubModelsV1ListHubModelNames"></a>
# **hubModelsV1ListHubModelNames**
> V1ListHubModelsResponse hubModelsV1ListHubModelNames(owner, offset, limit, sort, query)

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
    V1ListHubModelsResponse result = apiInstance.hubModelsV1ListHubModelNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1ListHubModelNames");
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

<a name="hubModelsV1ListHubModels"></a>
# **hubModelsV1ListHubModels**
> V1ListHubModelsResponse hubModelsV1ListHubModels(owner, offset, limit, sort, query)

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
    V1ListHubModelsResponse result = apiInstance.hubModelsV1ListHubModels(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1ListHubModels");
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

<a name="hubModelsV1PatchHubModel"></a>
# **hubModelsV1PatchHubModel**
> V1HubModel hubModelsV1PatchHubModel(owner, modelUuid, body)

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
    V1HubModel result = apiInstance.hubModelsV1PatchHubModel(owner, modelUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1PatchHubModel");
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

<a name="hubModelsV1UpdateHubModel"></a>
# **hubModelsV1UpdateHubModel**
> V1HubModel hubModelsV1UpdateHubModel(owner, modelUuid, body)

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
    V1HubModel result = apiInstance.hubModelsV1UpdateHubModel(owner, modelUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling HubModelsV1Api#hubModelsV1UpdateHubModel");
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


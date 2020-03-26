# DashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createDashboard**](DashboardsV1Api.md#createDashboard) | **POST** /api/v1/orgs/{owner}/dashboards | 
[**deleteDashboard**](DashboardsV1Api.md#deleteDashboard) | **DELETE** /api/v1/orgs/{owner}/dashboards/{uuid} | 
[**getDashboard**](DashboardsV1Api.md#getDashboard) | **GET** /api/v1/orgs/{owner}/dashboards/{uuid} | 
[**listDashboardNames**](DashboardsV1Api.md#listDashboardNames) | **GET** /api/v1/orgs/{owner}/dashboards/names | 
[**listDashboards**](DashboardsV1Api.md#listDashboards) | **GET** /api/v1/orgs/{owner}/dashboards | 
[**patchDashboard**](DashboardsV1Api.md#patchDashboard) | **PATCH** /api/v1/orgs/{owner}/dashboards/{dashboard.uuid} | 
[**updateDashboard**](DashboardsV1Api.md#updateDashboard) | **PUT** /api/v1/orgs/{owner}/dashboards/{dashboard.uuid} | 


<a name="createDashboard"></a>
# **createDashboard**
> V1Dashboard createDashboard(owner, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.createDashboard(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#createDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="deleteDashboard"></a>
# **deleteDashboard**
> deleteDashboard(owner, uuid)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.deleteDashboard(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#deleteDashboard");
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

<a name="getDashboard"></a>
# **getDashboard**
> V1Dashboard getDashboard(owner, uuid)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1Dashboard result = apiInstance.getDashboard(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#getDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listDashboardNames"></a>
# **listDashboardNames**
> V1ListDashboardsResponse listDashboardNames(owner, offset, limit, sort, query)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListDashboardsResponse result = apiInstance.listDashboardNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#listDashboardNames");
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="listDashboards"></a>
# **listDashboards**
> V1ListDashboardsResponse listDashboards(owner, offset, limit, sort, query)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListDashboardsResponse result = apiInstance.listDashboards(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#listDashboards");
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

[**V1ListDashboardsResponse**](V1ListDashboardsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="patchDashboard"></a>
# **patchDashboard**
> V1Dashboard patchDashboard(owner, dashboardUuid, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String dashboardUuid = "dashboardUuid_example"; // String | UUID
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.patchDashboard(owner, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#patchDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **dashboardUuid** | **String**| UUID |
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="updateDashboard"></a>
# **updateDashboard**
> V1Dashboard updateDashboard(owner, dashboardUuid, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.DashboardsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

DashboardsV1Api apiInstance = new DashboardsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String dashboardUuid = "dashboardUuid_example"; // String | UUID
V1Dashboard body = new V1Dashboard(); // V1Dashboard | Dashboard body
try {
    V1Dashboard result = apiInstance.updateDashboard(owner, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#updateDashboard");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **dashboardUuid** | **String**| UUID |
 **body** | [**V1Dashboard**](V1Dashboard.md)| Dashboard body |

### Return type

[**V1Dashboard**](V1Dashboard.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


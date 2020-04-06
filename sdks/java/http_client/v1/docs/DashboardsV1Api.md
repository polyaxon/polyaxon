# DashboardsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dashboardsV1CreateDashboard**](DashboardsV1Api.md#dashboardsV1CreateDashboard) | **POST** /api/v1/orgs/{owner}/dashboards | 
[**dashboardsV1DeleteDashboard**](DashboardsV1Api.md#dashboardsV1DeleteDashboard) | **DELETE** /api/v1/orgs/{owner}/dashboards/{uuid} | 
[**dashboardsV1GetDashboard**](DashboardsV1Api.md#dashboardsV1GetDashboard) | **GET** /api/v1/orgs/{owner}/dashboards/{uuid} | 
[**dashboardsV1ListDashboardNames**](DashboardsV1Api.md#dashboardsV1ListDashboardNames) | **GET** /api/v1/orgs/{owner}/dashboards/names | 
[**dashboardsV1ListDashboards**](DashboardsV1Api.md#dashboardsV1ListDashboards) | **GET** /api/v1/orgs/{owner}/dashboards | 
[**dashboardsV1PatchDashboard**](DashboardsV1Api.md#dashboardsV1PatchDashboard) | **PATCH** /api/v1/orgs/{owner}/dashboards/{dashboard.uuid} | 
[**dashboardsV1UpdateDashboard**](DashboardsV1Api.md#dashboardsV1UpdateDashboard) | **PUT** /api/v1/orgs/{owner}/dashboards/{dashboard.uuid} | 


<a name="dashboardsV1CreateDashboard"></a>
# **dashboardsV1CreateDashboard**
> V1Dashboard dashboardsV1CreateDashboard(owner, body)



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
    V1Dashboard result = apiInstance.dashboardsV1CreateDashboard(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1CreateDashboard");
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

<a name="dashboardsV1DeleteDashboard"></a>
# **dashboardsV1DeleteDashboard**
> dashboardsV1DeleteDashboard(owner, uuid)



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
    apiInstance.dashboardsV1DeleteDashboard(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1DeleteDashboard");
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

<a name="dashboardsV1GetDashboard"></a>
# **dashboardsV1GetDashboard**
> V1Dashboard dashboardsV1GetDashboard(owner, uuid)



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
    V1Dashboard result = apiInstance.dashboardsV1GetDashboard(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1GetDashboard");
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

<a name="dashboardsV1ListDashboardNames"></a>
# **dashboardsV1ListDashboardNames**
> V1ListDashboardsResponse dashboardsV1ListDashboardNames(owner, offset, limit, sort, query)



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
    V1ListDashboardsResponse result = apiInstance.dashboardsV1ListDashboardNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1ListDashboardNames");
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

<a name="dashboardsV1ListDashboards"></a>
# **dashboardsV1ListDashboards**
> V1ListDashboardsResponse dashboardsV1ListDashboards(owner, offset, limit, sort, query)



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
    V1ListDashboardsResponse result = apiInstance.dashboardsV1ListDashboards(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1ListDashboards");
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

<a name="dashboardsV1PatchDashboard"></a>
# **dashboardsV1PatchDashboard**
> V1Dashboard dashboardsV1PatchDashboard(owner, dashboardUuid, body)



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
    V1Dashboard result = apiInstance.dashboardsV1PatchDashboard(owner, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1PatchDashboard");
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

<a name="dashboardsV1UpdateDashboard"></a>
# **dashboardsV1UpdateDashboard**
> V1Dashboard dashboardsV1UpdateDashboard(owner, dashboardUuid, body)



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
    V1Dashboard result = apiInstance.dashboardsV1UpdateDashboard(owner, dashboardUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling DashboardsV1Api#dashboardsV1UpdateDashboard");
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


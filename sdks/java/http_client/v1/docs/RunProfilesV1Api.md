# RunProfilesV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**runProfilesV1CreateRunProfile**](RunProfilesV1Api.md#runProfilesV1CreateRunProfile) | **POST** /api/v1/orgs/{owner}/run_profiles | Create hub component
[**runProfilesV1DeleteRunProfile**](RunProfilesV1Api.md#runProfilesV1DeleteRunProfile) | **DELETE** /api/v1/orgs/{owner}/run_profiles/{uuid} | Delete hub component
[**runProfilesV1GetRunProfile**](RunProfilesV1Api.md#runProfilesV1GetRunProfile) | **GET** /api/v1/orgs/{owner}/run_profiles/{uuid} | Get hub component
[**runProfilesV1ListRunProfileNames**](RunProfilesV1Api.md#runProfilesV1ListRunProfileNames) | **GET** /api/v1/orgs/{owner}/run_profiles/names | List hub component names
[**runProfilesV1ListRunProfiles**](RunProfilesV1Api.md#runProfilesV1ListRunProfiles) | **GET** /api/v1/orgs/{owner}/run_profiles | List hub components
[**runProfilesV1PatchRunProfile**](RunProfilesV1Api.md#runProfilesV1PatchRunProfile) | **PATCH** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Patch hub component
[**runProfilesV1UpdateRunProfile**](RunProfilesV1Api.md#runProfilesV1UpdateRunProfile) | **PUT** /api/v1/orgs/{owner}/run_profiles/{run_profile.uuid} | Update hub component


<a name="runProfilesV1CreateRunProfile"></a>
# **runProfilesV1CreateRunProfile**
> V1RunProfile runProfilesV1CreateRunProfile(owner, body)

Create hub component

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1RunProfile body = new V1RunProfile(); // V1RunProfile | Artifact store body
try {
    V1RunProfile result = apiInstance.runProfilesV1CreateRunProfile(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1CreateRunProfile");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body |

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1DeleteRunProfile"></a>
# **runProfilesV1DeleteRunProfile**
> runProfilesV1DeleteRunProfile(owner, uuid)

Delete hub component

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    apiInstance.runProfilesV1DeleteRunProfile(owner, uuid);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1DeleteRunProfile");
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

<a name="runProfilesV1GetRunProfile"></a>
# **runProfilesV1GetRunProfile**
> V1RunProfile runProfilesV1GetRunProfile(owner, uuid)

Get hub component

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String uuid = "uuid_example"; // String | Uuid identifier of the entity
try {
    V1RunProfile result = apiInstance.runProfilesV1GetRunProfile(owner, uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1GetRunProfile");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **uuid** | **String**| Uuid identifier of the entity |

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1ListRunProfileNames"></a>
# **runProfilesV1ListRunProfileNames**
> V1ListRunProfilesResponse runProfilesV1ListRunProfileNames(owner, offset, limit, sort, query)

List hub component names

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunProfilesResponse result = apiInstance.runProfilesV1ListRunProfileNames(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1ListRunProfileNames");
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

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1ListRunProfiles"></a>
# **runProfilesV1ListRunProfiles**
> V1ListRunProfilesResponse runProfilesV1ListRunProfiles(owner, offset, limit, sort, query)

List hub components

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListRunProfilesResponse result = apiInstance.runProfilesV1ListRunProfiles(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1ListRunProfiles");
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

[**V1ListRunProfilesResponse**](V1ListRunProfilesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1PatchRunProfile"></a>
# **runProfilesV1PatchRunProfile**
> V1RunProfile runProfilesV1PatchRunProfile(owner, runProfileUuid, body)

Patch hub component

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String runProfileUuid = "runProfileUuid_example"; // String | UUID
V1RunProfile body = new V1RunProfile(); // V1RunProfile | Artifact store body
try {
    V1RunProfile result = apiInstance.runProfilesV1PatchRunProfile(owner, runProfileUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1PatchRunProfile");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **runProfileUuid** | **String**| UUID |
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body |

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="runProfilesV1UpdateRunProfile"></a>
# **runProfilesV1UpdateRunProfile**
> V1RunProfile runProfilesV1UpdateRunProfile(owner, runProfileUuid, body)

Update hub component

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RunProfilesV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

RunProfilesV1Api apiInstance = new RunProfilesV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String runProfileUuid = "runProfileUuid_example"; // String | UUID
V1RunProfile body = new V1RunProfile(); // V1RunProfile | Artifact store body
try {
    V1RunProfile result = apiInstance.runProfilesV1UpdateRunProfile(owner, runProfileUuid, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RunProfilesV1Api#runProfilesV1UpdateRunProfile");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **runProfileUuid** | **String**| UUID |
 **body** | [**V1RunProfile**](V1RunProfile.md)| Artifact store body |

### Return type

[**V1RunProfile**](V1RunProfile.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


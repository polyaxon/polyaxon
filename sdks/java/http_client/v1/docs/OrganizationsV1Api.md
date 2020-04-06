# OrganizationsV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**organizationsV1CreateOrganization**](OrganizationsV1Api.md#organizationsV1CreateOrganization) | **POST** /api/v1/orgs/create | 
[**organizationsV1CreateOrganizationMember**](OrganizationsV1Api.md#organizationsV1CreateOrganizationMember) | **POST** /api/v1/orgs/{owner}/members | 
[**organizationsV1DeleteOrganization**](OrganizationsV1Api.md#organizationsV1DeleteOrganization) | **DELETE** /api/v1/orgs/{owner} | 
[**organizationsV1DeleteOrganizationMember**](OrganizationsV1Api.md#organizationsV1DeleteOrganizationMember) | **DELETE** /api/v1/orgs/{owner}/members/{user} | 
[**organizationsV1GetOrganization**](OrganizationsV1Api.md#organizationsV1GetOrganization) | **GET** /api/v1/orgs/{owner} | 
[**organizationsV1GetOrganizationMember**](OrganizationsV1Api.md#organizationsV1GetOrganizationMember) | **GET** /api/v1/orgs/{owner}/members/{user} | 
[**organizationsV1ListOrganizationMembers**](OrganizationsV1Api.md#organizationsV1ListOrganizationMembers) | **GET** /api/v1/orgs/{owner}/members | 
[**organizationsV1ListOrganizationNames**](OrganizationsV1Api.md#organizationsV1ListOrganizationNames) | **GET** /api/v1/orgs/names | Get versions
[**organizationsV1ListOrganizations**](OrganizationsV1Api.md#organizationsV1ListOrganizations) | **GET** /api/v1/orgs/list | Get log handler
[**organizationsV1PatchOrganization**](OrganizationsV1Api.md#organizationsV1PatchOrganization) | **PATCH** /api/v1/orgs/{owner} | 
[**organizationsV1PatchOrganizationMember**](OrganizationsV1Api.md#organizationsV1PatchOrganizationMember) | **PATCH** /api/v1/orgs/{owner}/members/{member.user} | 
[**organizationsV1UpdateOrganization**](OrganizationsV1Api.md#organizationsV1UpdateOrganization) | **PUT** /api/v1/orgs/{owner} | 
[**organizationsV1UpdateOrganizationMember**](OrganizationsV1Api.md#organizationsV1UpdateOrganizationMember) | **PUT** /api/v1/orgs/{owner}/members/{member.user} | 


<a name="organizationsV1CreateOrganization"></a>
# **organizationsV1CreateOrganization**
> V1Organization organizationsV1CreateOrganization(body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
V1Organization body = new V1Organization(); // V1Organization | 
try {
    V1Organization result = apiInstance.organizationsV1CreateOrganization(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1CreateOrganization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**V1Organization**](V1Organization.md)|  |

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1CreateOrganizationMember"></a>
# **organizationsV1CreateOrganizationMember**
> V1OrganizationMember organizationsV1CreateOrganizationMember(owner, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1OrganizationMember body = new V1OrganizationMember(); // V1OrganizationMember | Organization body
try {
    V1OrganizationMember result = apiInstance.organizationsV1CreateOrganizationMember(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1CreateOrganizationMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body |

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1DeleteOrganization"></a>
# **organizationsV1DeleteOrganization**
> organizationsV1DeleteOrganization(owner)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
try {
    apiInstance.organizationsV1DeleteOrganization(owner);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1DeleteOrganization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1DeleteOrganizationMember"></a>
# **organizationsV1DeleteOrganizationMember**
> organizationsV1DeleteOrganizationMember(owner, user)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String user = "user_example"; // String | Memeber under namesapce
try {
    apiInstance.organizationsV1DeleteOrganizationMember(owner, user);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1DeleteOrganizationMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **user** | **String**| Memeber under namesapce |

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1GetOrganization"></a>
# **organizationsV1GetOrganization**
> V1Organization organizationsV1GetOrganization(owner)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
try {
    V1Organization result = apiInstance.organizationsV1GetOrganization(owner);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1GetOrganization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1GetOrganizationMember"></a>
# **organizationsV1GetOrganizationMember**
> V1OrganizationMember organizationsV1GetOrganizationMember(owner, user)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String user = "user_example"; // String | Memeber under namesapce
try {
    V1OrganizationMember result = apiInstance.organizationsV1GetOrganizationMember(owner, user);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1GetOrganizationMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **user** | **String**| Memeber under namesapce |

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizationMembers"></a>
# **organizationsV1ListOrganizationMembers**
> V1ListOrganizationMembersResponse organizationsV1ListOrganizationMembers(owner, offset, limit, sort, query)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
Integer offset = 56; // Integer | Pagination offset.
Integer limit = 56; // Integer | Limit size.
String sort = "sort_example"; // String | Sort to order the search.
String query = "query_example"; // String | Query filter the search search.
try {
    V1ListOrganizationMembersResponse result = apiInstance.organizationsV1ListOrganizationMembers(owner, offset, limit, sort, query);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1ListOrganizationMembers");
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

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizationNames"></a>
# **organizationsV1ListOrganizationNames**
> V1ListOrganizationsResponse organizationsV1ListOrganizationNames()

Get versions

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
try {
    V1ListOrganizationsResponse result = apiInstance.organizationsV1ListOrganizationNames();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1ListOrganizationNames");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1ListOrganizations"></a>
# **organizationsV1ListOrganizations**
> V1ListOrganizationsResponse organizationsV1ListOrganizations()

Get log handler

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
try {
    V1ListOrganizationsResponse result = apiInstance.organizationsV1ListOrganizations();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1ListOrganizations");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1PatchOrganization"></a>
# **organizationsV1PatchOrganization**
> V1Organization organizationsV1PatchOrganization(owner, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Organization body = new V1Organization(); // V1Organization | Organization body
try {
    V1Organization result = apiInstance.organizationsV1PatchOrganization(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1PatchOrganization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Organization**](V1Organization.md)| Organization body |

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1PatchOrganizationMember"></a>
# **organizationsV1PatchOrganizationMember**
> V1OrganizationMember organizationsV1PatchOrganizationMember(owner, memberUser, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String memberUser = "memberUser_example"; // String | User
V1OrganizationMember body = new V1OrganizationMember(); // V1OrganizationMember | Organization body
try {
    V1OrganizationMember result = apiInstance.organizationsV1PatchOrganizationMember(owner, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1PatchOrganizationMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **memberUser** | **String**| User |
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body |

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1UpdateOrganization"></a>
# **organizationsV1UpdateOrganization**
> V1Organization organizationsV1UpdateOrganization(owner, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
V1Organization body = new V1Organization(); // V1Organization | Organization body
try {
    V1Organization result = apiInstance.organizationsV1UpdateOrganization(owner, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1UpdateOrganization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **body** | [**V1Organization**](V1Organization.md)| Organization body |

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="organizationsV1UpdateOrganizationMember"></a>
# **organizationsV1UpdateOrganizationMember**
> V1OrganizationMember organizationsV1UpdateOrganizationMember(owner, memberUser, body)



### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OrganizationsV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

OrganizationsV1Api apiInstance = new OrganizationsV1Api();
String owner = "owner_example"; // String | Owner of the namespace
String memberUser = "memberUser_example"; // String | User
V1OrganizationMember body = new V1OrganizationMember(); // V1OrganizationMember | Organization body
try {
    V1OrganizationMember result = apiInstance.organizationsV1UpdateOrganizationMember(owner, memberUser, body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OrganizationsV1Api#organizationsV1UpdateOrganizationMember");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace |
 **memberUser** | **String**| User |
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body |

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


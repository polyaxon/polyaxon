# AuthV1Api

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthV1Api.md#login) | **POST** /api/v1/users/token | List runs


<a name="login"></a>
# **login**
> V1Auth login(body)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AuthV1Api;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AuthV1Api apiInstance = new AuthV1Api();
V1CredsBodyRequest body = new V1CredsBodyRequest(); // V1CredsBodyRequest | 
try {
    V1Auth result = apiInstance.login(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AuthV1Api#login");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**V1CredsBodyRequest**](V1CredsBodyRequest.md)|  |

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


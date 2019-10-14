# AuthServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthServiceApi.md#login) | **GET** /api/v1/users/token | List runs


<a name="login"></a>
# **login**
> V1Auth login(user, password)

List runs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.AuthServiceApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure API key authorization: ApiKey
ApiKeyAuth ApiKey = (ApiKeyAuth) defaultClient.getAuthentication("ApiKey");
ApiKey.setApiKey("YOUR API KEY");
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.setApiKeyPrefix("Token");

AuthServiceApi apiInstance = new AuthServiceApi();
String user = "user_example"; // String | User email.
String password = "password_example"; // String | Project where the experiement will be assigned.
try {
    V1Auth result = apiInstance.login(user, password);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling AuthServiceApi#login");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | **String**| User email. | [optional]
 **password** | **String**| Project where the experiement will be assigned. | [optional]

### Return type

[**V1Auth**](V1Auth.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


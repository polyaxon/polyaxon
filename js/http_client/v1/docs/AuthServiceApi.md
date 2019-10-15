# PolyaxonSdk.AuthServiceApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**login**](AuthServiceApi.md#login) | **POST** /api/v1/users/token | List runs


<a name="login"></a>
# **login**
> V1Auth login(body)

List runs

### Example
```javascript
var PolyaxonSdk = require('polyaxon-sdk');
var defaultClient = PolyaxonSdk.ApiClient.instance;

// Configure API key authorization: ApiKey
var ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

var apiInstance = new PolyaxonSdk.AuthServiceApi();

var body = new PolyaxonSdk.V1CredsBodyRequest(); // V1CredsBodyRequest | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.login(body, callback);
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


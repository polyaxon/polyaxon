# PolyaxonSdk.OrganizationsV1Api

Polyaxon sdk

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**approveOrganizationRuns**](OrganizationsV1Api.md#approveOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/approve | Approve cross-project runs selection
[**archiveOrganizationRuns**](OrganizationsV1Api.md#archiveOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/archive | Archive cross-project runs selection
[**bookmarkOrganizationRuns**](OrganizationsV1Api.md#bookmarkOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/bookmark | Bookmark cross-project runs selection
[**createOrganization**](OrganizationsV1Api.md#createOrganization) | **POST** /api/v1/orgs/create | Create organization
[**createOrganizationMember**](OrganizationsV1Api.md#createOrganizationMember) | **POST** /api/v1/orgs/{owner}/members | Create organization member
[**deleteOrganization**](OrganizationsV1Api.md#deleteOrganization) | **DELETE** /api/v1/orgs/{owner} | Delete organization
[**deleteOrganizationInvitation**](OrganizationsV1Api.md#deleteOrganizationInvitation) | **DELETE** /api/v1/orgs/{owner}/invitations | Delete organization invitation details
[**deleteOrganizationMember**](OrganizationsV1Api.md#deleteOrganizationMember) | **DELETE** /api/v1/orgs/{owner}/members/{name} | Delete organization member details
[**deleteOrganizationRuns**](OrganizationsV1Api.md#deleteOrganizationRuns) | **DELETE** /api/v1/orgs/{owner}/runs/delete | Delete cross-project runs selection
[**getOrganization**](OrganizationsV1Api.md#getOrganization) | **GET** /api/v1/orgs/{owner} | Get organization
[**getOrganizationActivities**](OrganizationsV1Api.md#getOrganizationActivities) | **GET** /api/v1/orgs/{owner}/activities | Get organization activities
[**getOrganizationInvitation**](OrganizationsV1Api.md#getOrganizationInvitation) | **GET** /api/v1/orgs/{owner}/invitations | Get organization invitation details
[**getOrganizationMember**](OrganizationsV1Api.md#getOrganizationMember) | **GET** /api/v1/orgs/{owner}/members/{name} | Get organization member details
[**getOrganizationRuns**](OrganizationsV1Api.md#getOrganizationRuns) | **GET** /api/v1/orgs/{owner}/runs | Get all runs in an organization
[**getOrganizationSettings**](OrganizationsV1Api.md#getOrganizationSettings) | **GET** /api/v1/orgs/{owner}/settings | Get organization settings
[**getOrganizationStats**](OrganizationsV1Api.md#getOrganizationStats) | **GET** /api/v1/orgs/{owner}/stats | Get organization stats
[**invalidateOrganizationRuns**](OrganizationsV1Api.md#invalidateOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/invalidate | Invalidate cross-project runs selection
[**listOrganizationMemberNames**](OrganizationsV1Api.md#listOrganizationMemberNames) | **GET** /api/v1/orgs/{owner}/members/names | Get organization member names
[**listOrganizationMembers**](OrganizationsV1Api.md#listOrganizationMembers) | **GET** /api/v1/orgs/{owner}/members | Get organization members
[**listOrganizationNames**](OrganizationsV1Api.md#listOrganizationNames) | **GET** /api/v1/orgs/names | List organizations names
[**listOrganizations**](OrganizationsV1Api.md#listOrganizations) | **GET** /api/v1/orgs/list | List organizations
[**organizationPlan**](OrganizationsV1Api.md#organizationPlan) | **POST** /api/v1/orgs/{owner}/plan | Organization plan
[**patchOrganization**](OrganizationsV1Api.md#patchOrganization) | **PATCH** /api/v1/orgs/{owner} | Patch organization
[**patchOrganizationInvitation**](OrganizationsV1Api.md#patchOrganizationInvitation) | **PATCH** /api/v1/orgs/{owner}/invitations | Patch organization invitation
[**patchOrganizationMember**](OrganizationsV1Api.md#patchOrganizationMember) | **PATCH** /api/v1/orgs/{owner}/members/{member.user} | Patch organization member
[**patchOrganizationSettings**](OrganizationsV1Api.md#patchOrganizationSettings) | **PATCH** /api/v1/orgs/{owner}/settings | Patch oranization settings
[**resendOrganizationInvitation**](OrganizationsV1Api.md#resendOrganizationInvitation) | **POST** /api/v1/orgs/{owner}/invitations | Resend organization invitation
[**restoreOrganizationRuns**](OrganizationsV1Api.md#restoreOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/restore | Restore cross-project runs selection
[**stopOrganizationRuns**](OrganizationsV1Api.md#stopOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/stop | Stop cross-project runs selection
[**tagOrganizationRuns**](OrganizationsV1Api.md#tagOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/tag | Tag cross-project runs selection
[**transferOrganizationRuns**](OrganizationsV1Api.md#transferOrganizationRuns) | **POST** /api/v1/orgs/{owner}/runs/transfer | Transfer cross-project runs selection to a new project
[**updateOrganization**](OrganizationsV1Api.md#updateOrganization) | **PUT** /api/v1/orgs/{owner} | Update organization
[**updateOrganizationInvitation**](OrganizationsV1Api.md#updateOrganizationInvitation) | **PUT** /api/v1/orgs/{owner}/invitations | Update organization invitation
[**updateOrganizationMember**](OrganizationsV1Api.md#updateOrganizationMember) | **PUT** /api/v1/orgs/{owner}/members/{member.user} | Update organization member
[**updateOrganizationSettings**](OrganizationsV1Api.md#updateOrganizationSettings) | **PUT** /api/v1/orgs/{owner}/settings | Update organization settings



## approveOrganizationRuns

> approveOrganizationRuns(owner, body)

Approve cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.approveOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## archiveOrganizationRuns

> archiveOrganizationRuns(owner, body)

Archive cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.archiveOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## bookmarkOrganizationRuns

> bookmarkOrganizationRuns(owner, body)

Bookmark cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.bookmarkOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## createOrganization

> V1Organization createOrganization(body)

Create organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let body = new PolyaxonSdk.V1Organization(); // V1Organization | 
apiInstance.createOrganization(body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## createOrganizationMember

> V1OrganizationMember createOrganizationMember(owner, body, opts)

Create organization member

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.createOrganizationMember(owner, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteOrganization

> deleteOrganization(owner, opts)

Delete organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'usage': "usage_example" // String | Owner usage query param.
};
apiInstance.deleteOrganization(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **usage** | **String**| Owner usage query param. | [optional] 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## deleteOrganizationInvitation

> deleteOrganizationInvitation(owner, opts)

Delete organization invitation details

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'member_user': "member_user_example", // String | User.
  'member_user_email': "member_user_email_example", // String | Read-only User email.
  'member_role': "member_role_example", // String | Role.
  'member_created_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional time when the entity was created.
  'member_updated_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional last time the entity was updated.
  'email': "email_example" // String | Optional email.
};
apiInstance.deleteOrganizationInvitation(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User. | [optional] 
 **member_user_email** | **String**| Read-only User email. | [optional] 
 **member_role** | **String**| Role. | [optional] 
 **member_created_at** | **Date**| Optional time when the entity was created. | [optional] 
 **member_updated_at** | **Date**| Optional last time the entity was updated. | [optional] 
 **email** | **String**| Optional email. | [optional] 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## deleteOrganizationMember

> deleteOrganizationMember(owner, name)

Delete organization member details

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.deleteOrganizationMember(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## deleteOrganizationRuns

> deleteOrganizationRuns(owner, body)

Delete cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.deleteOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## getOrganization

> V1Organization getOrganization(owner, opts)

Get organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'usage': "usage_example" // String | Owner usage query param.
};
apiInstance.getOrganization(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **usage** | **String**| Owner usage query param. | [optional] 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationActivities

> V1ListActivitiesResponse getOrganizationActivities(owner, opts)

Get organization activities

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.getOrganizationActivities(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListActivitiesResponse**](V1ListActivitiesResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationInvitation

> V1OrganizationMember getOrganizationInvitation(owner, opts)

Get organization invitation details

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'member_user': "member_user_example", // String | User.
  'member_user_email': "member_user_email_example", // String | Read-only User email.
  'member_role': "member_role_example", // String | Role.
  'member_created_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional time when the entity was created.
  'member_updated_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional last time the entity was updated.
  'email': "email_example" // String | Optional email.
};
apiInstance.getOrganizationInvitation(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User. | [optional] 
 **member_user_email** | **String**| Read-only User email. | [optional] 
 **member_role** | **String**| Role. | [optional] 
 **member_created_at** | **Date**| Optional time when the entity was created. | [optional] 
 **member_updated_at** | **Date**| Optional last time the entity was updated. | [optional] 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationMember

> V1OrganizationMember getOrganizationMember(owner, name)

Get organization member details

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let name = "name_example"; // String | Component under namesapce
apiInstance.getOrganizationMember(owner, name, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **name** | **String**| Component under namesapce | 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationRuns

> V1ListRunsResponse getOrganizationRuns(owner, opts)

Get all runs in an organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.getOrganizationRuns(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListRunsResponse**](V1ListRunsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationSettings

> V1Organization getOrganizationSettings(owner, opts)

Get organization settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'organization_user': "organization_user_example", // String | User.
  'organization_user_email': "organization_user_email_example", // String | Read-only User email.
  'organization_name': "organization_name_example", // String | Name.
  'organization_is_public': true, // Boolean | Optional flag to tell if this organization is public.
  'organization_created_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional time when the entity was created.
  'organization_updated_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional last time the entity was updated.
  'organization_support_revoke_at': new Date("2013-10-20T19:20:30+01:00"), // Date | Optional time to revoke support access.
  'organization_expiration': 56, // Number | Optional expiration for support.
  'organization_role': "organization_role_example", // String | Current user's role in this org.
  'organization_queue': "organization_queue_example", // String | Default queue.
  'organization_preset': "organization_preset_example", // String | Default preset.
  'organization_is_cloud_viewable': true // Boolean | Setting to enable viewable metadata on cloud.
};
apiInstance.getOrganizationSettings(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **organization_user** | **String**| User. | [optional] 
 **organization_user_email** | **String**| Read-only User email. | [optional] 
 **organization_name** | **String**| Name. | [optional] 
 **organization_is_public** | **Boolean**| Optional flag to tell if this organization is public. | [optional] 
 **organization_created_at** | **Date**| Optional time when the entity was created. | [optional] 
 **organization_updated_at** | **Date**| Optional last time the entity was updated. | [optional] 
 **organization_support_revoke_at** | **Date**| Optional time to revoke support access. | [optional] 
 **organization_expiration** | **Number**| Optional expiration for support. | [optional] 
 **organization_role** | **String**| Current user&#39;s role in this org. | [optional] 
 **organization_queue** | **String**| Default queue. | [optional] 
 **organization_preset** | **String**| Default preset. | [optional] 
 **organization_is_cloud_viewable** | **Boolean**| Setting to enable viewable metadata on cloud. | [optional] 

### Return type

[**V1Organization**](V1Organization.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getOrganizationStats

> Object getOrganizationStats(owner, opts)

Get organization stats

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'kind': "kind_example", // String | Stats Kind.
  'aggregate': "aggregate_example", // String | Stats aggregate.
  'groupby': "groupby_example", // String | Stats group.
  'trunc': "trunc_example" // String | Stats trunc.
};
apiInstance.getOrganizationStats(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **kind** | **String**| Stats Kind. | [optional] 
 **aggregate** | **String**| Stats aggregate. | [optional] 
 **groupby** | **String**| Stats group. | [optional] 
 **trunc** | **String**| Stats trunc. | [optional] 

### Return type

**Object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## invalidateOrganizationRuns

> invalidateOrganizationRuns(owner, body)

Invalidate cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.invalidateOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## listOrganizationMemberNames

> V1ListOrganizationMembersResponse listOrganizationMemberNames(owner, opts)

Get organization member names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listOrganizationMemberNames(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOrganizationMembers

> V1ListOrganizationMembersResponse listOrganizationMembers(owner, opts)

Get organization members

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let opts = {
  'offset': 56, // Number | Pagination offset.
  'limit': 56, // Number | Limit size.
  'sort': "sort_example", // String | Sort to order the search.
  'query': "query_example", // String | Query filter the search.
  'bookmarks': true, // Boolean | Filter by bookmarks.
  'pins': "pins_example", // String | Pinned entities.
  'mode': "mode_example", // String | Mode of the search.
  'no_page': true // Boolean | No pagination.
};
apiInstance.listOrganizationMembers(owner, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **offset** | **Number**| Pagination offset. | [optional] 
 **limit** | **Number**| Limit size. | [optional] 
 **sort** | **String**| Sort to order the search. | [optional] 
 **query** | **String**| Query filter the search. | [optional] 
 **bookmarks** | **Boolean**| Filter by bookmarks. | [optional] 
 **pins** | **String**| Pinned entities. | [optional] 
 **mode** | **String**| Mode of the search. | [optional] 
 **no_page** | **Boolean**| No pagination. | [optional] 

### Return type

[**V1ListOrganizationMembersResponse**](V1ListOrganizationMembersResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOrganizationNames

> V1ListOrganizationsResponse listOrganizationNames()

List organizations names

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
apiInstance.listOrganizationNames((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOrganizations

> V1ListOrganizationsResponse listOrganizations()

List organizations

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
apiInstance.listOrganizations((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**V1ListOrganizationsResponse**](V1ListOrganizationsResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## organizationPlan

> V1Organization organizationPlan(owner, body)

Organization plan

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body
apiInstance.organizationPlan(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## patchOrganization

> V1Organization patchOrganization(owner, body)

Patch organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body
apiInstance.patchOrganization(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## patchOrganizationInvitation

> V1OrganizationMember patchOrganizationInvitation(owner, body, opts)

Patch organization invitation

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.patchOrganizationInvitation(owner, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchOrganizationMember

> V1OrganizationMember patchOrganizationMember(owner, member_user, body, opts)

Patch organization member

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let member_user = "member_user_example"; // String | User
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.patchOrganizationMember(owner, member_user, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## patchOrganizationSettings

> V1Organization patchOrganizationSettings(owner, body)

Patch oranization settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body
apiInstance.patchOrganizationSettings(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## resendOrganizationInvitation

> V1OrganizationMember resendOrganizationInvitation(owner, body, opts)

Resend organization invitation

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.resendOrganizationInvitation(owner, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## restoreOrganizationRuns

> restoreOrganizationRuns(owner, body)

Restore cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.restoreOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## stopOrganizationRuns

> stopOrganizationRuns(owner, body)

Stop cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Uuids(); // V1Uuids | Uuids of the entities
apiInstance.stopOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1Uuids**](V1Uuids.md)| Uuids of the entities | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## tagOrganizationRuns

> tagOrganizationRuns(owner, body)

Tag cross-project runs selection

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1EntitiesTags(); // V1EntitiesTags | Data
apiInstance.tagOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1EntitiesTags**](V1EntitiesTags.md)| Data | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## transferOrganizationRuns

> transferOrganizationRuns(owner, body)

Transfer cross-project runs selection to a new project

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1EntitiesTransfer(); // V1EntitiesTransfer | Data
apiInstance.transferOrganizationRuns(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1EntitiesTransfer**](V1EntitiesTransfer.md)| Data | 

### Return type

null (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateOrganization

> V1Organization updateOrganization(owner, body)

Update organization

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body
apiInstance.updateOrganization(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


## updateOrganizationInvitation

> V1OrganizationMember updateOrganizationInvitation(owner, body, opts)

Update organization invitation

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.updateOrganizationInvitation(owner, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateOrganizationMember

> V1OrganizationMember updateOrganizationMember(owner, member_user, body, opts)

Update organization member

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let member_user = "member_user_example"; // String | User
let body = new PolyaxonSdk.V1OrganizationMember(); // V1OrganizationMember | Organization body
let opts = {
  'email': "email_example" // String | Optional email.
};
apiInstance.updateOrganizationMember(owner, member_user, body, opts, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **owner** | **String**| Owner of the namespace | 
 **member_user** | **String**| User | 
 **body** | [**V1OrganizationMember**](V1OrganizationMember.md)| Organization body | 
 **email** | **String**| Optional email. | [optional] 

### Return type

[**V1OrganizationMember**](V1OrganizationMember.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateOrganizationSettings

> V1Organization updateOrganizationSettings(owner, body)

Update organization settings

### Example

```javascript
import PolyaxonSdk from 'polyaxon-sdk';
let defaultClient = PolyaxonSdk.ApiClient.instance;
// Configure API key authorization: ApiKey
let ApiKey = defaultClient.authentications['ApiKey'];
ApiKey.apiKey = 'YOUR API KEY';
// Uncomment the following line to set a prefix for the API key, e.g. "Token" (defaults to null)
//ApiKey.apiKeyPrefix = 'Token';

let apiInstance = new PolyaxonSdk.OrganizationsV1Api();
let owner = "owner_example"; // String | Owner of the namespace
let body = new PolyaxonSdk.V1Organization(); // V1Organization | Organization body
apiInstance.updateOrganizationSettings(owner, body, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
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


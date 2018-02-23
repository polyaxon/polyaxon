body='{
"request": {
"branch":$1
}}'

curl -s -X POST \
   -H "Content-Type: application/json" \
   -H "Accept: application/json" \
   -H "Travis-API-Version: 3" \
   -H "Authorization: token 6SE268-eR1WMZUTvmYjUrg" \
   -d "$body" \
   https://api.travis-ci.org/repo/polyaxon%2Fpolyaxon-docker/requests

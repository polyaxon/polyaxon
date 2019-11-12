LOCAL_PORT=8010;
LOCAL_SWAGGER_FILE=`pwd`/swagger/v1/polyaxon_sdk.swagger.json;

docker run \
    -p ${LOCAL_PORT}:8080 \
    -e SWAGGER_JSON=/tmp/plx/swagger.json \
    -v ${LOCAL_SWAGGER_FILE}:/tmp/plx/swagger.json \
    swaggerapi/swagger-ui

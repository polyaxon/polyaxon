# Move generated swagger
mv swagger/v1/polyaxon_sdk.swagger.json swagger/v1/polyaxon_sdk_apis.swagger.json
# Copy upload files
cp swagger/upload.download/owner.artifact.swagger.json swagger/v1/owner.artifact.swagger.json
cp swagger/upload.download/project.artifact.swagger.json swagger/v1/project.artifact.swagger.json
cp swagger/upload.download/run.artifact.swagger.json swagger/v1/run.artifact.swagger.json
# Concat generated and upload files
jq -s '
	reduce .[] as $item ({}; . * $item) |
	.info.title = "Polyaxon SDKs and REST API specification." |
	.info.description = "Polyaxon SDKs and REST API specification." |
	.info.version = "1.0.0" |
	.info.contact = {"name": "Polyaxon sdk", "url": "https://github.com/polyaxon/polyaxon", "email": "contact@polyaxon.com"}
	' swagger/v1/{polyaxon_sdk_apis,owner.artifact,project.artifact,run.artifact}.swagger.json > "swagger/v1/polyaxon_sdk.swagger.json"
# Delete copied swagger files
rm swagger/v1/polyaxon_sdk_apis.swagger.json
rm swagger/v1/owner.artifact.swagger.json
rm swagger/v1/project.artifact.swagger.json
rm swagger/v1/run.artifact.swagger.json

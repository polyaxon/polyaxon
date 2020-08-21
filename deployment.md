 tracking
lyaxon deployment

## Starting polyaxon


```
docker pull polyaxon/polyaxon-npm-base
docker build -f platform/base/Dockerfile.dev -t polyaxon-base-dev .
docker-compose build
./cmd/serve
```

Update database
```
docker-compose run --rm api python3 ./polyaxon/manage.py migrate
```

Create super user
```
docker-compose run --rm api python3 ./polyaxon/manage.py createsuperuser
```

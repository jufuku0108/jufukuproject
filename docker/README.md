# Commands

```console
docker-compose up -d --force-recreate
docker-compose down
docker-compose exec web /bin/sh
for /f %T IN ('docker ps -a') DO docker rm %T
for /f %T IN ('docker images --format "{{.ID}}"') DO docker rmi %T

az acr login --name jufukuacr01.azurecr.io
az acr list --resource-group rg4containers --query "[].{acrLoginServer:loginServer}" --output table 

docker-compose push
```

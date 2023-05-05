# README

## Local Development

### Develop Docker image

- Download project

```console
git clone https://github.com/jufuku0108/jufukuproject.git

cd jufukuproject/docker
```

#### Unit development

- Change DB settings in docker/application/config/settings.py to use SQLITE for test.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ENGINE': os.environ.get("POSTGRES_ENGINE"),
        # 'NAME': os.environ.get("POSTGRES_DB"),
        # 'USER': os.environ.get("POSTGRES_USER"),
        # 'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        # 'HOST': os.environ.get("POSTGRES_HOST"),
        # 'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

```

- Change SECRET_KEY in the same file to test string.

```python
SECRET_KEY = "django-insecure--xxxxxxxxxxxx"
```

- Modify code and debug in docker/application folder and test run.

```console
python manage.py migrate
python manage.py runserver
```

#### Docker-compose development

- Change DB settings to use POSTGRESS and remove SQLITE db file.

```python
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': os.environ.get("POSTGRES_ENGINE"),
        'NAME': os.environ.get("POSTGRES_DB"),
        'USER': os.environ.get("POSTGRES_USER"),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': os.environ.get("POSTGRES_PORT"),
    }
}

```

- Change SECRET_KEY in the same file as below.

```python
SECRET_KEY = os.environ.get("SECRET_KEY")
```

- Run with other image using docker-compose.

```console
cd docker

docker-compose up -d --force-recreate

docker-compose down -v
```

#### Update image tab and upload

- Modify tag on docker-compose.yaml.
- Upload each images to ACR.

```console
az acr login --name jufukuacr01.azurecr.io

docker-compose push
```

### Running on docker-desktop

- Deploy Ingres on docker-desktop.

```comandline
kubectl config use-context docker-desktop

kubectl create namespace myapps 

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace myapps

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout rsa.key -out rsa.crt -subj "/CN=admin.jfadm170.net" -addext "subjectAltName = DNS:admin.jfadm170.net"

openssl pkcs12 -export -in rsa.crt -inkey rsa.key -out rsa.pfx

kubectl create secret tls jufuku-secret --key rsa.key --cert rsa.crt --namespace myapps

del rsa.*
```

- Make sure you have created latest image using docker-compose.
- Modify tag on values.yaml.
- Deploy resouces.

```comandline

helm upgrade --install jufukuproject-release ./helm --namespace myapps

kubectl port-forward --namespace=myapps service/ingress-nginx-controller 8080:443

```

- (options) Remove resouces from docker-desktop.

```comandline

helm uninstall jufukuproject-release -n=myapps

kubectl delete pvc jufuku-vol-static-pvc -n=myapps

kubectl delete pvc my-vol-jufuku-db-sttflst-0 -n=myapps
```

## Deploy to Azure

### Create AKS

```comandline
az aks create --resource-group rg4containers --name jufukuk8s01 --node-count 1 --generate-ssh-keys --attach-acr jufukuacr01

az aks update -n jufukuk8s01 -g rg4containers --enable-disk-driver --enable-file-driver 

az aks enable-addons --addons azure-keyvault-secrets-provider --name jufukuk8s01 --resource-group rg4containers

az aks update -g rg4containers -n jufukuk8s01 --enable-managed-identity

az aks show -g rg4containers -n jufukuk8s01 --query addonProfiles.azureKeyvaultSecretsProvider.identity.clientId -o tsv
```

### Create Cert Manager and Ingress Controller for AKS

```comandline
az aks get-credentials --resource-group rg4containers --name jufukuk8s01

cd azure

kubectl create namespace myapps 

kubectl apply -f jufuku-secret-provider.yaml -n myapps

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx --namespace myapps --set controller.ingressClassResource.name=ingress-nginx --set controller.replicaCount=2 --set controller.nodeSelector."kubernetes\.io/os"=linux --set defaultBackend.nodeSelector."kubernetes\.io/os"=linux --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz -f t2-ingress-controller.yaml

az acr import --name jufukuacr01 --source quay.io/jetstack/cert-manager-controller:v1.8.0 --image jetstack/cert-manager-controller:v1.8.0

az acr import --name jufukuacr01 --source quay.io/jetstack/cert-manager-webhook:v1.8.0 --image jetstack/cert-manager-webhook:v1.8.0

az acr import --name jufukuacr01 --source quay.io/jetstack/cert-manager-cainjector:v1.8.0 --image jetstack/cert-manager-cainjector:v1.8.0

kubectl label namespace myapps cert-manager.io/disable-validation=true

helm repo add jetstack https://charts.jetstack.io

helm repo update

helm install cert-manager jetstack/cert-manager --namespace myapps --version=v1.8.0 --set installCRDs=true --set nodeSelector."kubernetes\.io/os"=linux --set image.repository=jufukuacr01.azurecr.io/jetstack/cert-manager-controller --set image.tag=v1.8.0 --set webhook.image.repository=jufukuacr01.azurecr.io/jetstack/cert-manager-webhook --set webhook.image.tag=v1.8.0 --set cainjector.image.repository=jufukuacr01.azurecr.io/jetstack/cert-manager-cainjector --set cainjector.image.tag=v1.8.0

kubectl apply -f jufuku-cluster-issuer.yaml --namespace myapps

```

## Depoy resources on Aks

```comandline
az aks get-credentials --resource-group rg4containers --name jufukuk8s01

helm upgrade --install jufukuproject-release ./helm --namespace myapps -f ./helm/prodvalues.yaml

```

## Upload git

- Remove secret strings from prodvalues.yaml
- Upload git

```comandline
git add -A

git commit -m "update"

git push -u origin main
```

## Useful commands for trouble shooting

```commandline
kubectl -n kubernetes-dashboard create token admin-user

kubectl get ingressclass --all-namespaces

kubectl delete ingressclass ingress-nginx

kubectl get validatingwebhookconfigurations  --all-namespaces

kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission

Foreach($x in (kubectl api-resources --verbs=list --namespaced -o name)){ kubectl get --show-kind --ignore-not-found -n ingress-basic $x }      

kubectl patch ns ingress-basic -p {\"metadata\":{\"finalizers\":null}} --type=merge
```

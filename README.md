# Helm

```comandline
git remote add origin https://github.com/jufuku0108/jufukuproject.git

git push origin HEAD:main --force

```

## Local debug commands

```comandline
kubectl config get-contexts
kubectl config current-context
kubectl config use-context docker-desktop

kubectl create namespace myapps 


helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace myapps

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout rsa.key -out rsa.crt -subj "/CN=admin.jfadm170.net" -addext "subjectAltName = DNS:admin.jfadm170.net"
openssl pkcs12 -export -in rsa.crt -inkey rsa.key -out rsa.pfx
kubectl create secret tls jufuku-secret --key rsa.key --cert rsa.crt --namespace myapps
del rsa.*

helm repo add myrepo https://jufuku0108.github.io/jufukuproject/
helm repo update
helm upgrade --install jufukuproject-release myrepo/jufukuproject --namespace myapps

kubectl port-forward --namespace=myapps service/ingress-nginx-controller 8080:443


kubectl -n kubernetes-dashboard create token admin-user

helm uninstall jufukuproject-release -n=myapps
kubectl delete pvc jufuku-vol-static-pvc -n=myapps
kubectl delete pvc my-vol-jufuku-db-sttflst-0 -n=myapps
```

## Create k8s instance

```comandline
az aks create --resource-group rg4containers --name jufukuk8s01 --node-count 1 --generate-ssh-keys --attach-acr jufukuacr01
az aks update -n jufukuk8s01 -g rg4containers --enable-disk-driver --enable-file-driver 
az aks enable-addons --addons azure-keyvault-secrets-provider --name jufukuk8s01 --resource-group rg4containers
az aks update -g rg4containers -n jufukuk8s01 --enable-managed-identity
az aks show -g rg4containers -n jufukuk8s01 --query addonProfiles.azureKeyvaultSecretsProvider.identity.clientId -o tsv

```

## Create Cert Manager and Ingress Controller for Azure

```comandline
az aks get-credentials --resource-group rg4containers --name jufukuk8s01

kubectl create namespace myapps 

kubectl apply -f t2-secret-provider.yaml -n myapps

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

kubectl apply -f t2-cluster-issuer.yaml --namespace myapps

kubectl apply -f t2-ingress.yaml --namespace myapps

```

## Depoy resources

```comandline
az aks get-credentials --resource-group rg4containers --name jufukuk8s01

kubectl apply -f t2-configmap.yaml -n myapps
kubectl apply -f t2-vol-static.yaml -n myapps
kubectl apply -f t2-db.yaml -n myapps
kubectl apply -f t2-web.yaml -n myapps

```

## Trouble shooring

```commandline
kubectl get ingressclass --all-namespaces
kubectl delete ingressclass ingress-nginx

kubectl get validatingwebhookconfigurations  --all-namespaces
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission

Foreach($x in (kubectl api-resources --verbs=list --namespaced -o name)){ kubectl get --show-kind --ignore-not-found -n ingress-basic $x }      
kubectl patch ns ingress-basic -p {\"metadata\":{\"finalizers\":null}} --type=merge
```

# 🚀 DevOps Challenge

This project implements a **cloud-native Flask API service** that echoes request headers, HTTP method, and body. It is containerized using Docker, deployed to Kubernetes via Helm, monitored with Prometheus, and secured using OPA Gatekeeper. CI/CD is powered by GitHub Actions.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Clone Repository](#clone-repository)
  - [Run Locally](#run-locally)
  - [Build Docker Image](#build-docker-image)
  - [Run Container Tests](#run-container-tests)
  - [Deploy to Kubernetes](#deploy-to-kubernetes)
  - [Monitor Metrics](#monitor-metrics)
  - [Apply OPA Policies](#apply-opa-policies)
  - [Run Helm Test](#run-helm-test)
- [CI/CD Pipeline](#cicd-pipeline)
- [Screenshots](#screenshots)
- [Notes](#notes)
- [License](#license)

---

## ✅ Overview

The Flask-based API responds to requests on the `/api` endpoint and returns an HTML page with:

- Request headers
- HTTP method
- JSON body

### Key Features:

- ✅ Dockerized (multi-stage build with non-root user)
- ✅ Kubernetes-ready with Helm (Service, Ingress, RBAC)
- ✅ CI/CD with GitHub Actions
- ✅ OPA policies for secure deployment
- ✅ Prometheus metrics at `/metrics`
- ✅ Follows Twelve-Factor App principles

### Example API Test
```bash
curl --header "Content-Type: application/json" \
     --data '{"username":"xyz","password":"xyz"}' \
     http://${URL}:${PORT}/api
```

---

## 🔧 Prerequisites

### Tools

Ensure the following tools are installed:

```bash
git --version
python3 --version
docker --version
minikube version
helm version
kubectl version --client
```

Install `container-structure-test`:
```bash
curl -LO https://storage.googleapis.com/container-structure-test/latest/container-structure-test-linux-amd64
chmod +x container-structure-test-linux-amd64
sudo mv container-structure-test-linux-amd64 /usr/local/bin/container-structure-test
```

### Accounts

- GitHub account (for CI/CD)
- Docker Hub account (for pushing images)

---

## 🚀 Setup Instructions

### 📁 Clone Repository

```bash
git https://github.com/chndel-abhishek/tradesocio-devops-challenge.git
cd tradesocio-devops-challenge
```

---

### 🧪 Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
python app/main.py
```

Test the API:
```bash
curl --header "Content-Type: application/json" \
     --data '{"username":"xyz","password":"xyz"}' \
     http://localhost:5000/api
```

Expected output (HTML page with request details).

---

### 🐳 Build Docker Image

```bash
docker build -t tradesocio-devops-challenge .
docker run -p 5000:5000 tradesocio-devops-challenge
```

Test the running container:
```bash
curl --header "Content-Type: application/json" \
     --data '{"username":"xyz","password":"xyz"}' \
     http://localhost:5000/api
```

---

### 🔍 Run Container Tests

```bash
container-structure-test test \
  --image tradesocio-devops-challenge \
  --config tests/container-test.yaml
```

Expected Output:  
✅ Python installed  
✅ App file exists  
✅ Runs as non-root user

---

### ☸️ Deploy to Kubernetes

```bash
minikube start
minikube addons enable ingress
```

Install with Helm:
```bash
helm install devops-challenge ./helm/devops-challenge \
  --set ingress.host=$(minikube ip).nip.io
```

Verify pods:
```bash
kubectl get pods
```

Test via Ingress:
```bash
curl --header "Content-Type: application/json" \
     --data '{"username":"xyz","password":"xyz"}' \
     http://$(minikube ip).nip.io/api
```

---

### 📈 Monitor Metrics

```bash
curl http://$(minikube ip).nip.io/metrics
```

Expected Output (partial):
```
# HELP api_requests_total Total API requests
# TYPE api_requests_total counter
api_requests_total{method="POST",endpoint="/api"} 1.0
```

#### (Optional) Deploy Prometheus

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus --set server.service.type=ClusterIP
kubectl port-forward svc/prometheus-server 9090:80 -n default
```

Access Prometheus:  
[http://localhost:9090](http://localhost:9090)  
Query: `api_requests_total`

---

### 🔒 Apply OPA Policies

Install OPA Gatekeeper:
```bash
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system --create-namespace
```

Apply policies:
```bash
kubectl apply -f opa-policy.yaml
```

Expected Output:
```
constrainttemplate.templates.gatekeeper.sh/k8snondefaultsa configured
constrainttemplate.templates.gatekeeper.sh/k8snonrootcontainer configured
k8snondefaultsa.constraints.gatekeeper.sh/non-default-sa created
k8snonrootcontainer.constraints.gatekeeper.sh/non-root-container created
```

Test policy enforcement:
```bash
kubectl apply -f test-non-compliant.yaml
```

Expected:
```
Error from server (Forbidden): admission webhook "validation.gatekeeper.sh" denied the request...
```

---

### 🧪 Run Helm Test

```bash
helm test devops-challenge
```

Expected Output:  
✅ Test pod runs and successfully connects to the deployed service.

---

## 🔁 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) handles:

- 🛠 Building the Docker image
- ✅ Running unit tests (`tests/test_api.py`)
- ✅ Running container tests (`tests/container-test.yaml`)
- 🚀 Pushing image to Docker Hub on `main` branch push

### Setup Secrets in GitHub:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

---

## 📸 Screenshots

### API Response
```bash
curl --header "Content-Type: application/json" \
     --data '{"username":"xyz","password":"xyz"}' \
     http://$(minikube ip).nip.io/api
```
![API RESPONSE](https://github.com/chndel-abhishek/tradesocio-devops-challenge/blob/main/pictures/api-response.png?raw=true)

### Prometheus Metrics
```bash
curl http://$(minikube ip).nip.io/metrics
```
![PROMETHEUS METRICS](https://github.com/chndel-abhishek/tradesocio-devops-challenge/blob/main/pictures/prometheus-metrics.png?raw=true)
### Kubernetes Pods
```bash
kubectl get pods
```
![API POD](https://github.com/chndel-abhishek/tradesocio-devops-challenge/blob/main/pictures/pods.png?raw=true)

### OPA Policy Enforcement
```bash
kubectl apply -f test-non-compliant.yaml
```
![OPA GATEKEEPER](https://github.com/chndel-abhishek/tradesocio-devops-challenge/blob/main/pictures/opa-gatekeeper.png?raw=true)

### GitHub Actions CI/CD
Check the Actions tab for successful pipeline runs.

---
![CICD](https://github.com/chndel-abhishek/tradesocio-devops-challenge/blob/main/pictures/cicd.png?raw=true)


## 📝 Notes

- The `/metrics` endpoint exposes Prometheus metrics.
- Helm chart includes hooks for pre-install migration and Helm testing.
- OPA enforces:
  - 🔐 No usage of default ServiceAccounts
  - 🔐 All containers run as non-root

---

## 🛠 TODO

- [ ] Expand unit tests to cover edge cases (e.g., malformed JSON)
- [ ] Add Grafana dashboards for visual metrics
- [ ] Implement external secrets management (e.g., Vault)
- [ ] Add HorizontalPodAutoscaler (HPA) for autoscaling

---

## 📄 License

This project is licensed under the **MIT License**.  
See [`LICENSE`](LICENSE) file for details.

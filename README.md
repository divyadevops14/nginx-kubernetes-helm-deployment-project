# 🚀 Nginx on Kubernetes | Helm & Jenkins CI/CD

Deploy Nginx on Kubernetes using **Helm and Jenkins**! This project demonstrates automated application deployment, chart validation, and CI/CD pipeline integration.

## 📁 Project Structure

```text
nginx-kubernetes-helm-deployment-project/
│
├── .gitignore              # Ignores sensitive and temporary files
├── README.md               # Project documentation
│
├── myapp/                  # Nginx Helm chart
│   ├── Chart.yaml          # Chart name, version, and metadata
│   ├── values.yaml         # Default configurable deployment settings
│   └── templates/          # Kubernetes resource templates
│       ├── _helpers.tpl    # Reusable Helm template functions
│       ├── configmap.yaml  # Application configuration
│       ├── deployment.yaml # Nginx pods, image, and replicas
│       └── service.yaml    # Application network access
│
└── jenkins/
    └── Jenkinsfile         # Automated CI/CD pipeline
```

**Helm configuration:** `values.yaml` stores default settings consumed by the templates. These may include the container image, replica count, and service configuration. The exact keys depend on the contents of your file.

## 🔄 CI/CD Workflow

```text
GitHub → Jenkins → Helm Validation
                    ↓
              Manifest Validation
                    ↓
               Helm Deploy
                    ↓
          Kubernetes (Docker Desktop)
                    ↓
               Nginx App
                    ↓
                 Verify
```

## 🛠️ Tech Stack

Kubernetes | Helm | Jenkins | Docker Desktop | Git | GitHub | Nginx

## 📋 Prerequisites

Before deployment, make sure you have:

- **Docker Desktop** – Kubernetes enabled and running.
- **kubectl** – To communicate with the Kubernetes cluster.
- **Helm** – To validate and deploy the chart.
- **Jenkins** – To execute the CI/CD pipeline.
- **Git** – To clone and manage the repository.

Check your installations:

```bash
docker --version
kubectl version --client
helm version
git --version
java -version
```

Check that Kubernetes is running:

```bash
kubectl get nodes
```

## 🚀 Quick Deployment

**1. Clone the repository**

```bash
git clone https://github.com/divyadevops14/nginx-kubernetes-helm-deployment-project.git
cd nginx-kubernetes-helm-deployment-project
```

**2. Validate the chart**

```bash
helm lint myapp/
helm template myapp myapp/
```

**3. Deploy using Helm**

```bash
helm upgrade --install myapp myapp/ -n dev --create-namespace
```

**4. Verify deployment**

```bash
kubectl get pods -n dev
kubectl get deployments -n dev
helm status myapp -n dev
```

**5. Access Nginx**

```bash
kubectl port-forward -n dev service/myapp-myapp 8080:80
```

Open: [http://localhost:8080](http://localhost:8080)

## ⚙️ Jenkins Pipeline

| Stage | Action |
|---|---|
| Checkout | Fetch code from GitHub |
| Helm Lint | Validate Helm chart |
| Manifest Validation | Generate Kubernetes manifests |
| Deploy | Install or upgrade using Helm |
| Verify | Check deployment and pods |

## ✅ Deployment Results

- **Helm Release:** `myapp` — Deployed
- **Namespace:** `dev`
- **Replicas:** 2
- **Pods:** 2/2 Running
- **Deployment:** 2/2 Available
- **Jenkins:** Pipeline successful

## ⭐ Key Learnings

- Created reusable Helm charts.
- Deployed Nginx on Kubernetes.
- Automated deployment using Jenkins.
- Integrated GitHub with Jenkins.
- Validated and verified Kubernetes resources.

**Environment:** Local Docker Desktop Kubernetes — no active AWS EKS cluster required.

---

**Built as part of my AWS DevOps interview preparation.**

⭐ Kubernetes | Helm | Jenkins | Docker | GitHub
# 🚀 Nginx Kubernetes Deployment Using Helm & Jenkins

Automated Kubernetes application deployment using **Helm, Jenkins CI/CD, Docker Desktop Kubernetes, and GitHub**. This project demonstrates Helm chart validation, automated deployments, and Kubernetes workload verification through a Jenkins pipeline.

---

## Repository Layout

```text
nginx-kubernetes-helm-deployment-project/
│
├── myapp/
│   ├── Chart.yaml              # Helm chart metadata
│   ├── values.yaml             # Configurable deployment values
│   └── templates/
│       ├── _helpers.tpl        # Reusable Helm template helpers
│       ├── configmap.yaml      # Application configuration
│       ├── deployment.yaml     # Kubernetes Deployment
│       └── service.yaml        # Kubernetes Service
│
├── jenkins/
│   └── Jenkinsfile             # Automated CI/CD pipeline
│
└── README.md                   # Project documentation
```

---

## What This Project Deploys

```text
GitHub Repository
       │
       ▼
Jenkins CI/CD Pipeline
       │
       ├── Checkout Source Code
       │
       ├── Helm Chart Lint
       │
       ├── Validate Kubernetes Manifests
       │
       ├── Deploy / Upgrade Using Helm
       │
       └── Verify Deployment
                 │
                 ▼
       Docker Desktop Kubernetes
                 │
                 ▼
          Nginx Application
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Kubernetes | Container orchestration |
| Helm | Kubernetes package management |
| Jenkins | CI/CD pipeline automation |
| Docker Desktop | Local Kubernetes environment |
| Git & GitHub | Source code management |
| Nginx | Web server |

---

## Quick Start

### Step 1 — Check Prerequisites

Install and configure:
- Docker Desktop with Kubernetes enabled
- kubectl
- Helm
- Jenkins
- Git

### Step 2 — Clone the Repository

```bash
git clone https://github.com/divyadevops14/nginx-kubernetes-helm-deployment-project.git
cd nginx-kubernetes-helm-deployment-project
```

### Step 3 — Validate the Helm Chart

```bash
helm lint myapp/
helm template myapp myapp/
```

### Step 4 — Deploy the Application

```bash
helm upgrade --install myapp myapp/ -n dev --create-namespace
```

### Step 5 — Verify the Deployment

```bash
kubectl get pods -n dev
kubectl get deployments -n dev
kubectl get services -n dev
helm status myapp -n dev
```

### Step 6 — Access Nginx Locally

```bash
kubectl port-forward -n dev service/myapp-myapp 8080:80
```

Open `http://localhost:8080` in your browser while port forwarding is running.

---

## Jenkins CI/CD Pipeline

The `jenkins/Jenkinsfile` automates the application deployment workflow.

```text
Checkout → Helm Lint → Manifest Validation → Helm Deploy → Verify
```

| Stage | Purpose |
|---|---|
| Checkout | Retrieves project code from GitHub |
| Helm Chart Lint | Checks Helm chart structure and configuration |
| Manifest Validation | Renders Kubernetes manifests for validation |
| Deploy with Helm | Installs or upgrades the application |
| Verify | Checks Kubernetes pods and Helm release status |

---

## Deployment Verification

The application was successfully deployed to the local Kubernetes cluster.

- **Helm Release:** `myapp`
- **Namespace:** `dev`
- **Application:** Nginx
- **Replicas:** 2
- **Pod Status:** Running
- **Deployment Status:** Successful

---

## Key Highlights

- Automated Kubernetes deployment through Jenkins.
- Reusable and configurable Helm chart.
- Automated Helm chart and manifest validation.
- Repeatable application installation and upgrades.
- Kubernetes workload and release verification.
- Practical experience with Git-based CI/CD workflows.

---

## Project Goal

Built as a hands-on project for **AWS DevOps interview preparation**, focusing on Kubernetes, Helm, Jenkins, Git, and CI/CD automation.

**Note:** This project currently runs on local Docker Desktop Kubernetes. It does not require an active AWS EKS cluster.

---

⭐ If you find this project useful, feel free to explore the repository!

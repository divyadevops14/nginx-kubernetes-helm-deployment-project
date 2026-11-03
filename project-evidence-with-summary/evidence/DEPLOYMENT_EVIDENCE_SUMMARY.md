# Deployment Evidence & Verification Summary

**Project:** Nginx on Kubernetes with Helm & Jenkins CI/CD  
**Evidence captured:** October 31, 2026 (timestamps visible in terminal and Jenkins screenshots)  
**Environment:** Docker Desktop Kubernetes (local `kind` cluster)  
**Status:** Successful deployment and pipeline verification shown in the supplied screenshots

---

## Executive Summary

This document summarizes the supplied screenshots showing an Nginx application packaged with a custom Helm chart and deployed to a local Kubernetes cluster. The evidence covers Helm chart validation, Helm release installation/status, Kubernetes workload health, Docker Desktop cluster status, Jenkins pipeline execution, and browser access to the Nginx welcome page.

The screenshots demonstrate a successful local deployment workflow. They do not establish production readiness or a GitHub webhook trigger.

---

## Phase 1: Local Kubernetes Environment

### Docker Desktop Kubernetes Cluster

**Evidence:** `02-docker-desktop-kubernetes-cluster.jpg`

The Docker Desktop Kubernetes dashboard shows:

- Cluster status: **Active**
- Cluster type: `kind`
- Nodes: `1`
- Kubernetes version: `v1.36.1`
- Node: `desktop-control-plane`
- Node status: **Ready**
- Docker engine: Running

The dashboard also shows the `myapp-myapp` deployment as **Available**, with **2/2** pods, and both listed pods in **Running** status.

---

## Phase 2: Helm Chart Validation

### Helm Lint

**Evidence:** `03-helm-chart-validation-and-install.jpg`

**Command executed:**

```powershell
helm lint .\myapp
```

**Observed output:**

```text
[INFO] Chart.yaml: icon is recommended
1 chart(s) linted, 0 chart(s) failed
```

**Result:**
- Helm chart lint completed.
- No chart lint failures were reported.
- Helm displayed an optional recommendation to add a chart icon.

---

## Phase 3: Helm Release Installation

### Helm Install

**Evidence:** `03-helm-chart-validation-and-install.jpg`

**Command executed:**

```powershell
helm install myapp .\myapp
```

**Observed result:**

```text
NAME: myapp
NAMESPACE: default
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
```

The screenshot shows the release installed in the `default` namespace for this run.

### Helm Release Status in the `dev` Namespace

**Evidence:** `04-helm-deployment-status-and-pods.jpg`

A separate Git Bash screenshot shows:

```bash
helm status myapp -n dev
```

**Observed result:**

```text
NAME: myapp
NAMESPACE: dev
STATUS: deployed
REVISION: 1
DESCRIPTION: Install complete
```

This screenshot represents a deployment/status check in the `dev` namespace. The supplied screenshots therefore show evidence from runs in both `default` and `dev`; these should be treated as separate runs/configurations.

---

## Phase 4: Kubernetes Deployment Verification

### Deployment and Pod Status

**Evidence:** `03-helm-chart-validation-and-install.jpg` and `04-helm-deployment-status-and-pods.jpg`

The PowerShell screenshot shows:

```bash
kubectl get deployments
kubectl get pods -w
kubectl get svc
helm status myapp
```

**Observed deployment result:**

| Resource | Name | Observed status |
|---|---|---|
| Deployment | `myapp-myapp` | 2/2 Ready, 2 available |
| Pod | `myapp-myapp-8dbb8cc6b-fmd56` | 1/1 Running |
| Pod | `myapp-myapp-8dbb8cc6b-wtpbk` | 1/1 Running |
| Service | `myapp-myapp` | ClusterIP, port 80/TCP |

The Git Bash screenshot separately shows the `dev` namespace with:
- Deployment `myapp-myapp`: **2/2 Ready**
- Two application pods: **1/1 Running**
- Pod restarts: **0**
- Service `myapp-myapp`: **ClusterIP**, port **80/TCP**

The Git Bash screenshot displays the service ClusterIP as `10.96.90.182`; the PowerShell screenshot displays `10.96.71.159`. These are values from separate captured runs and are not expected to be identical.

---

## Phase 5: Application Access Verification

### Port Forwarding

**Evidence:** `04-helm-deployment-status-and-pods.jpg`

**Command executed:**

```bash
kubectl port-forward -n dev service/myapp-myapp 8080:80
```

**Observed output:**

```text
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
```

This confirms that kubectl established local port forwarding from port `8080` to service port `80` for the `dev` namespace.

### Nginx Browser Verification

**Evidence:** `06-nginx-welcome-page.jpg`

The browser screenshot shows the Nginx welcome page at:

```text
http://localhost:8080
```

The page displays **“Welcome to nginx!”**, demonstrating that the application responded through the local port-forwarded endpoint.

---

## Phase 6: Jenkins CI/CD Pipeline

### Jenkins Pipeline Execution

**Evidence:** `05-jenkins-pipeline-success.jpg`

**Pipeline job:** `nginx-Kubernetes-helm-deployment-project`  
**Build shown:** `#1`  
**Displayed result:** Successful (green stage cells)  
**Displayed average full run time:** Approximately 21 seconds

| Stage | Displayed duration | Result |
|---|---:|---|
| Declarative: Checkout SCM | 2s | Passed |
| Checkout | 2s | Passed |
| Lint Helm Chart | 1s | Passed |
| Deploy with Helm | 10s | Passed |
| Verify | 1s | Passed |

The Jenkins Stage View shows all five stages completed successfully.

**What the pipeline demonstrates:**
- Source checkout from the configured SCM.
- Helm chart linting.
- Helm-based deployment.
- A verification stage after deployment.

The screenshot proves a successful Jenkins build. It does not, by itself, prove that a GitHub webhook automatically triggered the build.

---

## Phase 7: Evidence Inventory

| Screenshot | Evidence provided |
|---|---|
| `01-project-overview.svg` | Architecture and end-to-end workflow illustration |
| `02-docker-desktop-kubernetes-cluster.jpg` | Active local Kubernetes cluster, ready node, available deployment and running pods |
| `03-helm-chart-validation-and-install.jpg` | Helm lint, release installation, deployment, pods and service output |
| `04-helm-deployment-status-and-pods.jpg` | Helm release status in `dev`, two running pods and port-forwarding output |
| `05-jenkins-pipeline-success.jpg` | Successful Jenkins pipeline stages |
| `06-nginx-welcome-page.jpg` | Nginx welcome page in the browser |

---

## Key Learnings Demonstrated

1. **Helm chart validation** — checking a chart with `helm lint`.
2. **Helm release management** — installing and inspecting a release with Helm.
3. **Kubernetes workload verification** — checking Deployments, Pods and Services.
4. **Local application access** — forwarding a Kubernetes Service to a local browser port.
5. **CI/CD automation** — using Jenkins stages for checkout, linting, deployment and verification.
6. **Evidence-based verification** — keeping screenshots of the cluster, pipeline and application output.

---

## Conclusion

The supplied evidence demonstrates that:

- The Docker Desktop Kubernetes cluster was active and its node was Ready.
- The Helm chart lint completed with zero failures.
- Helm reported the `myapp` release as deployed.
- The application Deployment showed two available replicas and two running pods.
- Kubernetes port forwarding was established on local port `8080`.
- The Nginx welcome page was visible in the browser.
- The Jenkins pipeline build shown completed all displayed stages successfully.

**Overall result:** Successful local Nginx deployment using Kubernetes, Helm and Jenkins, as demonstrated by the supplied screenshots.

---

**Evidence note:** This summary records only details visible in the supplied screenshots. The screenshots include separate deployment runs using the `default` and `dev` namespaces; verify the active namespace and cluster before reproducing commands.

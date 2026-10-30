# Application Deployment Using Helm

A small Flask app packaged as a **Helm chart** and deployed to a **local Kubernetes cluster**
(no AWS / EKS costs). Includes separate dev / staging / prod configs, health probes,
autoscaling, upgrade + rollback, and a Jenkins pipeline.

## Architecture

```
 Developer -> GitHub -> Jenkins -> docker build -> helm lint -> helm upgrade --install -> Kubernetes
                                                                                   |
                                                       Deployment (pods) <- ConfigMap
                                                            |
                                                         Service -> (Ingress optional)
```

## Project structure

```
helm-app-deployment/
├── app/
│   ├── app.py              # Flask app (/, /health)
│   ├── requirements.txt
│   └── Dockerfile
├── helm/myapp/
│   ├── Chart.yaml          # chart name + versions
│   ├── values.yaml         # defaults
│   ├── values-dev.yaml     # env overrides
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── _helpers.tpl    # reusable names/labels
│       ├── configmap.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml    # only if ingress.enabled
│       ├── hpa.yaml        # only if autoscaling.enabled
│       └── NOTES.txt
├── Jenkinsfile
└── README.md
```

## Prerequisites

Docker Desktop (with Kubernetes enabled) **or** minikube / kind, plus `kubectl` and `helm`.

```bash
docker --version
kubectl version --client
helm version
kubectl config get-contexts     # pick a LOCAL context, e.g. docker-desktop / minikube / kind-kind
```

## Step 1: Build the image

```bash
cd helm-app-deployment
docker build -t myapp:1.0.0 app/
```

Load it into your cluster (Docker Desktop shares images automatically; others need this):

```bash
minikube image load myapp:1.0.0        # minikube
kind load docker-image myapp:1.0.0     # kind
```

## Step 2: Validate the chart (no cluster needed)

```bash
helm lint helm/myapp
helm template myapp helm/myapp -f helm/myapp/values-dev.yaml     # view generated YAML
helm install myapp helm/myapp --dry-run --debug -n dev
```

## Step 3: Deploy to dev

```bash
helm upgrade --install myapp helm/myapp \
  -n dev --create-namespace \
  -f helm/myapp/values-dev.yaml

helm list -n dev
kubectl get pods,svc -n dev
```

Access the app:

```bash
kubectl port-forward svc/myapp-myapp 8080:80 -n dev
# open http://localhost:8080      -> {"environment":"dev", ...}
```

## Step 4: Other environments

```bash
helm upgrade --install myapp-staging helm/myapp -n staging --create-namespace -f helm/myapp/values-staging.yaml
helm upgrade --install myapp-prod    helm/myapp -n prod    --create-namespace -f helm/myapp/values-prod.yaml
```

Same chart, different values: that is the main benefit of Helm.

## Step 5: Upgrade, scale and rollback (demo this!)

```bash
# Scale with --set
helm upgrade myapp helm/myapp -n dev -f helm/myapp/values-dev.yaml --set replicaCount=3
kubectl get pods -n dev

# Change the message (ConfigMap change restarts pods automatically)
helm upgrade myapp helm/myapp -n dev -f helm/myapp/values-dev.yaml --set app.greeting="Version 2!"

# Break it on purpose
helm upgrade myapp helm/myapp -n dev -f helm/myapp/values-dev.yaml --set image.tag=does-not-exist
kubectl get pods -n dev          # ImagePullBackOff / ErrImagePull

# Roll back
helm history myapp -n dev
helm rollback myapp 2 -n dev
helm status myapp -n dev
```

## Step 6: Jenkins pipeline

The `Jenkinsfile` runs: Checkout -> Helm lint -> Docker build -> Helm deploy -> Verify (auto rollback on failure).

Requirements for the Jenkins machine/agent: `docker`, `helm` and `kubectl` on PATH, and a kubeconfig that
points at your local cluster (Jenkins must run on the same machine as the cluster, or be given its kubeconfig).
Create a Pipeline job -> "Pipeline script from SCM" -> your GitHub repo.

## Cleanup

```bash
helm uninstall myapp -n dev
helm uninstall myapp-staging -n staging
helm uninstall myapp-prod -n prod
kubectl delete ns dev staging prod
```

## What to explain in a viva / interview

- **Why Helm?** Templating, one chart for many environments, versioned releases, one-command rollback.
- **Chart vs release:** a chart is the package; a release is one installed instance of it.
- **values.yaml:** defaults, overridden by `-f file` and then by `--set` (right-most wins).
- **checksum/config annotation:** changing the ConfigMap changes the pod template, so pods restart.
- **Probes:** readiness gates traffic; liveness restarts a stuck container.
- **HPA:** enabled only in prod; `replicas` is omitted from the Deployment when HPA is on.
- **Rollback:** `helm history` + `helm rollback <release> <revision>`.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| `ImagePullBackOff` | Image not in cluster. Load it (`minikube image load` / `kind load`) and keep `pullPolicy: IfNotPresent` |
| `CrashLoopBackOff` | `kubectl logs <pod> -n dev` |
| `helm lint` YAML error | Indentation in templates; run `helm template` to see where |
| Pods Pending | Not enough resources; lower `resources` or `replicaCount` |
| Jenkins can't reach cluster | Wrong/missing kubeconfig for the Jenkins user |

#!/usr/bin/env bash

k3d cluster delete workflows-ci || true
k3d cluster create --config bootstrap/k3d.conf

# Prevent users from accidentally deploying to the wrong cluster.
currentContext=$(kubectl config current-context)
if [ "$currentContext" == "k3d-workflows-ci" ]; then
    echo "Starting deployment to cluster..."
else
    echo "The kubectl context is not what we expected. Exiting for safety. Perhaps the k3d cluster failed to create?"
    exit 1
fi

# Deploy Argo CD, which in turn deploys everything else
kubectl -n kube-system rollout status deployment/metrics-server
kubectl apply -k bootstrap/argocd
kubectl -n argocd rollout status statefulset/argocd-application-controller
kubectl -n argocd rollout status deployment/argocd-repo-server
kubectl apply -k bootstrap/argocd
kubectl -n argocd apply -f bootstrap/app-of-apps"${1}"

# Create 'final-application' namespace for the final application
kubectl create namespace final-application

# Wait for Argo CD to start syncing its new-found applications
sleep 30
kubectl -n nfs-server-provisioner rollout status statefulset/nfs-server-provisioner
kubectl -n ingress-nginx rollout status deployment/nginx-ingress-nginx-controller
kubectl -n ingress-nginx rollout status daemonset/svclb-nginx-ingress-nginx-controller
kubectl -n argo rollout status deployment/workflow-controller
kubectl -n argo rollout status deployment/argo-server
kubectl -n minio rollout status deployment/minio

echo "Complete. You should be able to navigate to https://localhost:8443/argo/workflows/argo in your browser now. (Remember to accept the self-signed SSL cert)."

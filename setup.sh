#!/bin/bash

k3d cluster create --config bootstrap/k3d.conf

# Prevent users from accidentally deploying to the wrong cluster.
currentContext=$(kubectl config current-context)
if [ "$currentContext" == "k3d-workflows-ci" ]; then
    echo "Starting deployment to cluister..."
else
    echo "The kubectl context is not what we expected. Exiting for safety. Perhaps the k3d cluster failed to create?"
    exit 1
fi

# Deploy Argo CD, which in turn deploys everything else
kubectl apply -k bootstrap/argocd
kubectl -n argocd rollout status statefulset/argocd-application-controller
kubectl -n argocd rollout status deployment/argocd-repo-server
kubectl -n argocd apply -f bootstrap/app-of-apps

# Wait for Argo CD to start syncing its new-found applications
sleep 30
kubectl -n nfs-server-provisioner rollout status statefulset/nfs-server-provisioner
kubectl -n ingress-nginx rollout status deployment/nginx-ingress-nginx-controller
kubectl -n ingress-nginx rollout status daemonset/svclb-nginx-ingress-nginx-controller
kubectl -n argo rollout status deployment/workflow-controller
kubectl -n argo rollout status deployment/argo-server

echo "Complete. You should be able to navigate to https://localhost:8443/workflows/argo?limit=500 in your browser now. (Remember to accept the self-signed SSL cert)."
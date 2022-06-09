#!/bin/bash

# Create cluster and deploy argocd, which in turn deploys the rest of the applications
k3d cluster create --config bootstrap/k3d.conf
kubectl apply -k bootstrap/argocd
kubectl -n argocd rollout status statefulset/argocd-application-controller
kubectl -n argocd rollout status deployment/argocd-repo-server
kubectl -n argocd apply -f bootstrap/app-of-apps

# Wait for argoCD to start syncing its new-found applications
sleep 30
kubectl -n nfs-server-provisioner rollout status statefulset/nfs-server-provisioner
kubectl -n ingress-nginx rollout status deployment/nginx-ingress-nginx-controller
kubectl -n ingress-nginx rollout status daemonset/svclb-nginx-ingress-nginx-controller
kubectl -n argo rollout status deployment/workflow-controller
kubectl -n argo rollout status deployment/argo-server

echo "Complete. You should be able to navigate to https://localhost:8443/workflows/argo?limit=500 in your browser now. (Remember to accept the self-signed SSL cert)."
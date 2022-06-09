#!/bin/bash

# if k3d is already running cluster 'workflows-ci', delete it
k3d cluster delete workflows-ci

# Create cluster and deploy argocd, which in turn deploys the rest of the applications
k3d cluster create --config bootstrap/k3d.conf
kubectl apply -k bootstrap/argocd
kubectl -n argocd rollout status statefulset/argocd-application-controller
kubectl -n argocd rollout status deployment/argocd-repo-server
kubectl -n argocd apply -f bootstrap/app-of-apps

sleep 30
kubectl -n nfs-server-provisioner rollout status statefulset/nfs-server-provisioner
kubectl -n argo rollout status deployment/workflow-controller
kubectl -n argo rollout status deployment/argo-server
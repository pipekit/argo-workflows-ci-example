#!/bin/bash

# if k3d is already running cluster 'workflows-ci', delete it
k3d cluster delete workflows-ci

# Create cluster and deploy argocd
k3d cluster create --config bootstrap/k3d.conf
kubectl apply -k bootstrap/argocd
kubectl -n argocd apply -f bootstrap/applications
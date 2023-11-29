from shared import (
    Resource
)

#Leverages Argo Workflows' ability to interact directly with Kubernetes to deploy an Argo CD Application.
#It monitors the health status of the application and is only considered 'done' once the Argo CD
#Application reports itself as healthy.

deploy_application_manifest = '''apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: final-application
  finalizers:
    - resources-finalizer.argocd.argoproj.io
  namespace: argocd
spec:
  destination:
    namespace: final-application
    server: 'https://kubernetes.default.svc'
  project: default
  source:
    path: bootstrap/final-application
    repoURL: 'https://github.com/pipekit/argo-workflows-ci-example.git'
    targetRevision: HEAD
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - PrunePropagationPolicy=background
      - PruneLast=true
      - CreateNamespace=true
'''

deploy_application = Resource(name="deploy-application",
                              action="create",
                              success_condition="status.health.status == Healthy",
                              failure_condition="status.health.status == Degraded",
                              manifest=deploy_application_manifest
                              )

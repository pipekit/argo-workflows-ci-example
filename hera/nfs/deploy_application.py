from hera.workflows import WorkflowTemplate, DAG, Resource, Task
from hera.exceptions import AlreadyExists
import shared

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

with WorkflowTemplate(
    name="hera-deploy-application",
    entrypoint="main",
    namespace=shared.namespace,
    annotations={
        'workflows.argoproj.io/description': """Leverages Argo Workflows' ability to interact directly with Kubernetes to deploy an Argo CD Application.
It monitors the health status of the application and is only considered 'done' once the Argo CD
Application reports itself as healthy.""",
        'workflows.argoproj.io/maintainer': 'Pipekit Inc',
        'workflows.argoproj.io/maintainer_url': 'https://github.com/pipekit/argo-workflows-ci-example',
        'workflows.argoproj.io/version': '>= 3.3.6',
    },
) as deploy_application:
    deploy_application_resource = Resource(name="deploy-application",
                  action="create",
                  success_condition="status.health.status == Healthy",
                  failure_condition="status.health.status == Degraded",
                  manifest=deploy_application_manifest
                  )
    with DAG(name="main") as main:
        Task(name="deploy-application", template=deploy_application_resource)

try:
    deploy_application.create()
except AlreadyExists:
    deploy_application.update()

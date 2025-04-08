from shared import (
    Resource
)

# Leverages Argo Workflows' ability to interact directly with Kubernetes to deploy a Kubernetes resource.
# It monitors the health status of the Kubernetes resource and is only considered 'done' once
# the resource reports itself as healthy.

deploy_resource_manifest_svc = '''apiVersion: v1
kind: Service
metadata:
  name: example-application
  namespace: final-application
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 80
  selector:
    app: example-application
'''

deploy_resource_manifest_ingress = '''apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-application
  namespace: final-application
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    nginx.ingress.kubernetes.io/use-regex: 'true'
spec:
  ingressClassName: nginx
  rules:
  - host: localhost
    http:
      paths:
      - path: /workflows-ci-example/(.*)
        pathType: Prefix
        backend:
          service:
            name: example-application
            port:
              number: 80
  tls:
  - hosts:
    - localhost
    secretName: tls.localhost
'''

deploy_resource_manifest_deployment = '''apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: example-application
  namespace: final-application
  labels:
    app: example-application
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 10}
      - setWeight: 40
      - pause: {duration: 10}
      - setWeight: 60
      - pause: {duration: 10}
      - setWeight: 80
      - pause: {duration: 10}
  selector:
    matchLabels:
      app: example-application
  template:
    metadata:
      labels:
        app: example-application
    spec:
      containers:
        - name: eg-app
          image: k3d-registry.localhost:5001/hello-world:{{workflow.parameters.container_tag}}
          imagePullPolicy: Always
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /
              port: 80
              scheme: HTTP
            initialDelaySeconds: 5
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
          resources:
            requests:
              cpu: 3m
              memory: 20Mi
            limits:
              cpu: 10m
              memory: 64Mi
'''

deploy_resource_svc = Resource(name="deploy-resource-svc",
                              action="apply",
                              manifest=deploy_resource_manifest_svc
                              )
deploy_resource_ingress = Resource(name="deploy-resource-ingress",
                            action="apply",
                            manifest=deploy_resource_manifest_ingress
                            )
deploy_resource_deployment = Resource(name="deploy-resource-deployment",
                            action="apply",
                            success_condition="status.phase == Healthy",
                            manifest=deploy_resource_manifest_deployment
                            )

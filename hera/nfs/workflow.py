from hera.workflows import Workflow, Parameter, DAG, Container, Task, Resource
from ci_workflow import ci_workflow

import shared

with Workflow(
    generate_name="hera-ci-workflow-",
    namespace="argo",
    labels={
        'argoworkflows.argoproj.io/workflow-template': 'hera-ci-workflow',
    },
    arguments=[
        Parameter(name="app_repo", value="argo-workflows-ci-example"),
        Parameter(name="git_branch", value="main"),
        Parameter(name="target_branch", value="main"),
        Parameter(name="container_tag", value="stable"),
        Parameter(name="container_image", value="k3d-registry.localhost:5000/hello-world"),
        Parameter(name="dockerfile", value="Dockerfile"),
        Parameter(name="path", value="/CI"),
    ],
    workflow_template_ref=ci_workflow
) as workflow:
    workflow.create()

from shared import (
    Workflow,
    Parameter
)

from ci_rollouts_workflow import ci_rollouts_workflow

with Workflow(
    generate_name="hera-rollouts-workflow-",
    namespace="argo",
    labels={
        'argoworkflows.argoproj.io/workflow-template': 'hera-rollouts-workflow',
    },
    arguments=[
        Parameter(name="app_repo", value="argo-workflows-ci-example"),
        Parameter(name="git_branch", value="main"),
        Parameter(name="target_branch", value="main"),
        Parameter(name="container_tag", value="new"),
        Parameter(name="container_image", value="k3d-registry.localhost:5000/hello-world"),
        Parameter(name="dockerfile", value="Dockerfile"),
        Parameter(name="path", value="/CI"),
    ],
    workflow_template_ref=ci_rollouts_workflow
) as workflow:
    workflow.create()
    print(workflow.get_workflow_link())   # get a link for monitoring
    print("Waiting for workflow to complete")
    workflow.wait()

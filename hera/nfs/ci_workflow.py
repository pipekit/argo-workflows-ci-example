from hera.workflows import WorkflowTemplate, Parameter, DAG, Container, Task, Resource, EmptyDirVolume, models as m
from hera.exceptions import AlreadyExists

from git_checkout_pr import git_checkout_pr
from html_modifier import html_modifier
from container_build import container_build
from deploy_application import deploy_application, deploy_application_manifest
import shared

with WorkflowTemplate(
    name="hera-ci-workflow",
    entrypoint="main",
    namespace=shared.namespace,
    volume_claim_templates=[
        m.PersistentVolumeClaim(
            metadata=m.ObjectMeta(name="workdir"),
            spec=m.PersistentVolumeClaimSpec(
                access_modes=['ReadWriteMany'],
                storage_class_name='nfs',
                resources=m.ResourceRequirements(
                    requests={
                        "storage": m.Quantity(__root__="1Gi"),
                    }
                ),
            ),
        )
    ],
        # The container build step copies the code from the NFS share to this ephemeral volume, and then runs the build.
        # We do this a) because NFS shares are slow and b) to allow us to run another workflow step alongside the build if we wish.
    volumes=[EmptyDirVolume(name="container-build")],
    arguments=[
        Parameter(name="app_repo", value=""),
        Parameter(name="git_branch", value=""),
        Parameter(name="target_branch", value=""),
        Parameter(name="container_tag", value=""),
        Parameter(name="container_image", value=""),
        Parameter(name="dockerfile", value=""),
        Parameter(name="path", value=""),
    ],
    annotations={
        'workflows.argoproj.io/description': '''A basic CI leveraging Argo Workflows.

The Workflow...

* pulls a repo from git. Specifically pulling a branch based on a pull request;
* merges the target branch into it;
* modifies the html that will be copied into the container to inject the unique name of the running workflow;
* builds a container from a Dockerfile and pushes to a registry;
* deploys an Argo CD application that uses the newly-built container to deploy a static website.

It does not pretend to be a definitive example, but it aims to inspire. In order to make this a semi-usable example, we have cut a number of security corners. Please don't just blindly run this in production.
''',
        'workflows.argoproj.io/maintainer': 'Pipekit Inc',
        'workflows.argoproj.io/maintainer_url': 'https://github.com/pipekit/argo-workflows-ci-example',
        'workflows.argoproj.io/version': '>= 3.3.6',
    },
) as ci_workflow:
    delete_application_resource = Resource(name="delete-application",
                  action="delete",
                  manifest=deploy_application_manifest
                  )
    with DAG(name="main") as main:
        git_checkout_task = Task(name="git-checkout", template_ref=m.TemplateRef(
            name=git_checkout_pr.name, template=git_checkout_pr.entrypoint))
        html_modifier_task = Task(name="html-modifier", template_ref=m.TemplateRef(
            name=html_modifier.name, template=html_modifier.entrypoint))
        container_build_task = Task(name="container-build", template_ref=m.TemplateRef(
            name=container_build.name, template=container_build.entrypoint))
        deploy_application_task = Task(name="deploy-application", template_ref=m.TemplateRef(
            name=deploy_application.name, template=deploy_application.entrypoint))
        delete_application_task = delete_application_resource(name="delete-application", depends="deploy-application.Failed")
        git_checkout_task >> html_modifier_task >> container_build_task >> deploy_application_task

ci_workflow.to_file(".")
try:
    ci_workflow.create()
except AlreadyExists:
    ci_workflow.update()

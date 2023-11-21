from hera.workflows import WorkflowTemplate, DAG, Container, Task, Resources, models as m
from hera.exceptions import AlreadyExists
import shared

html_modifier_script = '''apk --update add git

cd /workdir
echo "Start Clone of source branch"
git clone https://github.com/pipekit/{{workflow.parameters.app_repo}}.git
cd {{workflow.parameters.app_repo}}

## These lines are a hack just for the example.
git config --global --add safe.directory /workdir/{{workflow.parameters.app_repo}}
git config --global user.email "sales@pipekit.io"
git config --global user.name "Tim Collins"

git checkout {{workflow.parameters.git_branch}}

echo "Merge in target branch"
git merge origin/{{workflow.parameters.target_branch}}

echo "Complete."
'''

with WorkflowTemplate(
    name="hera-html-modifier",
    entrypoint="main",
    namespace=shared.namespace,
    annotations={
        'workflows.argoproj.io/description': 'Performs a sed command to inject the current running Workflow name into a given file.',
        'workflows.argoproj.io/maintainer': 'Pipekit Inc',
        'workflows.argoproj.io/maintainer_url': 'https://github.com/pipekit/argo-workflows-ci-example',
        'workflows.argoproj.io/version': '>= 3.3.6',
    },
) as html_modifier:
    html_modifier_cont = Container(name="html-modifier",
                                     image="ubuntu:latest",
                                     command=["sh", "-c", html_modifier_script],
                                     volume_mounts=[
                                         m.VolumeMount(name="workdir",
                                                       mount_path="/workdir")],
                                     resources=Resources(memory_request="256Mi", cpu_request="100m"),
                                     active_deadline_seconds=1200)
    with DAG(name="main") as main:
        Task(name="html-modifier", template=html_modifier_cont)

try:
    html_modifier.create()
except AlreadyExists:
    html_modifier.update()

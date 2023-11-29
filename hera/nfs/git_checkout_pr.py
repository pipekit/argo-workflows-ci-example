from shared import (
    WorkflowTemplate,
    Resources,
    Container,
    m
)

# Clones a git repository and then performs a git checkout of a branch defined in the workflow workflow.parameters. Then merges in a defined target branch.

git_checkout_script = '''apk --update add git

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

git_checkout_pr = Container(name="git-checkout-pr",
               image="alpine:latest",
               command=["sh", "-c", git_checkout_script],
               volume_mounts=[
                   m.VolumeMount(name="workdir",
                                 mount_path="/workdir")],
               resources=Resources(memory_request="250Mi", cpu_request="4m"),
               active_deadline_seconds=1200)

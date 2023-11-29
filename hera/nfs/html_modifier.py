from shared import (
    Container,
    Resources,
    m
)

# Performs a sed command to inject the current running Workflow name into a given file.

html_modifier_script = '''cd /workdir/{{workflow.parameters.app_repo}}/CI

if grep -q CHANGEMEPLEASE index.html; then
  cat index.html | sed -E 's/CHANGEMEPLEASE/{{workflow.name}} and it used nfs-server-provisioner for artifact passing./g' > tmp_index.html
  mv tmp_index.html index.html
else
  echo "CHANGEMEPLEASE was not found in index.html. Exiting"
  exit 1
fi

cat index.html
'''

html_modifier = Container(name="html-modifier",
                               image="ubuntu:latest",
                               command=["sh", "-c", html_modifier_script],
                               volume_mounts=[
                                   m.VolumeMount(name="workdir",
                                                 mount_path="/workdir")],
                               resources=Resources(memory_request="256Mi", cpu_request="100m"),
                               active_deadline_seconds=1200)

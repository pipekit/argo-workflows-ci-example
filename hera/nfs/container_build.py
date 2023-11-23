from shared import (
    Container,
    Env,
    Resources,
    m
)

container_build_script = '''echo "Retrieving git clone..." && cp -R /workdir/{{workflow.parameters.app_repo}} /container-build && \
buildctl-daemonless.sh build \
--frontend \
dockerfile.v0 \
--local \
context=/container-build/{{workflow.parameters.app_repo}}{{workflow.parameters.path}} \
--local \
dockerfile=/container-build/{{workflow.parameters.app_repo}}{{workflow.parameters.path}} \
--opt filename={{workflow.parameters.dockerfile}} \
--output \
type=image,name={{workflow.parameters.container_image}}:{{workflow.parameters.container_tag}},push=true,registry.insecure=true
'''

# Uses Buildkit to build a container image within Kubernetes.
container_build = Container(name="container-build",
                            image="moby/buildkit:v0.12.3-rootless",
                            command=["sh", "-c", container_build_script],
                            env=[
                                Env(name="BUILDKITD_FLAGS",
                                    value="--oci-worker-no-process-sandbox")],
                            volume_mounts=[
                                m.VolumeMount(name="container-build",
                                              mount_path="/container-build"),
                                m.VolumeMount(name="workdir",
                                              mount_path="/workdir")],
                            resources=Resources(memory_request="1Gi", cpu_request="1"),
                            security_context=m.SecurityContext(seccomp_profile=m.SeccompProfile(type="Unconfined"),
                                                               run_as_user=1000,
                                                               run_as_group=1000,),
                            active_deadline_seconds=1200)

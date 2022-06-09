# argo-workflows-ci-example
A basic CI leveraging Argo Workflows.

## The Workflow...
* pulls a repo from git. Specifically pulling a branch based on a pull request;
* merges the target branch into it;
* modifies the html that will be copied into the container to inject the unique name of the running workflow;
* builds a container from a Dockerfile and pushes to a registry;
* deploys an Argo CD application that uses the newly-built container to deploy a static website.

It does not pretend to be a definitive example, but it aims to inspire.
In order to make this a semi-usable example, we have cut a number of security corners. Please don't just blindly run this in production.

## Prerequisites
### Running Locally
In order to run this locally, you will need [k3d](https://k3d.io/) installed, as well as kubectl.
### Running on a remote cluster
The summary is "probably don't". If you really want to run on a remote cluster, you will need to use an empty cluster that you don't care about. This script blindly installs and configures a number of tools and has no regard for what you already have installed. It also makes assumptions about things like the container registry URL and ingress URLS that you will need to manually change in order to make it work.

## Steps to Run
```
chmod +x setup.sh
./setup.sh
```
Once the setup is completed (3-7 mins depending on how sprightly your cluster is feeling), you can view the argo-workflows UI at https://localhost:8443/workflows/argo?limit=500 (the S in https is important and you'll need to accept the self-signed certificate). Make sure you are looking at the 'argo' namespace.

Then you can deploy the workflow and you should see it appear in the UI.
```
kubectl -n argo create -f workflow.yml 
```

Once the workflow has successfuly run, you can navigate to https://localhost:8443/argo-workflows-ci-example/ in your browser. The website should tell you the branch that it was built from (the default is 'example') and the name of the workflow that built it.

You can delete the Argocd CD application to remove the deployment. You should do this before re-running the workflow:
```
kubectl -n argocd delete application final-application
```

If you wish, you can modify the parameters in workflow.yml as follows and you'll build from our second example branch:
```
    parameters:
      - name: app_repo
        value: "argo-workflows-ci-example"
      - name: git_branch
        value: 'another-example'
      - name: target_branch
        value: 'main'
      - name: container_tag
        value: 'stable'
      - name: container_image
        value: "k3d-registry.localhost:5000/hello-world"
      - name: dockerfile
        value: Dockerfile
      - name: path
        value: "/CI"
```

You can of course adjust other paramaters as you see fit, and keep running the workflows to experiment. You may need to change the final-application deployment.

# Running in production
This is a very simplified workflow aiming to highlight what's possible using Argo Workflows. Some things to consider when running in production:

* Triggering the CI using Argo Events. We have include an example of how to do this in the [TODO.md](TODO.md) file.
* Storing secrets more sensibly and injecting them only when required. We use Hashicorp Vault to achieve this. We strongly advise against putting any secret into git.
* Leveraging things like AWS spot instances and the cluster autoscaler to keep node costs down.
* Using much more restrictive Argo CD and Argo Workflows RBAC policies.
* Using something like the [ci-github-notifier](https://github.com/sendible-labs/ci-github-notifier) to annotate pull requests and branches with the status of your CI.
* Use dedicated images for the job. Don't pull alpine and install git on each run, use a custom alpine-git image. We just did the example this way to reduce the number of dependencies required to get up and running.


# So what's happening?
todo
## Prometheus metrics.
todo
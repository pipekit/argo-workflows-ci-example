# argo-workflows-ci-example
A basic CI leveraging Argo Workflows.

## The Workflow...
* pulls a repo from git. Spefically pulling a branch based on a pull request;
* Tests that the PR branch is mergeable into its target;
* simulates a unit test;
* builds a container from a dockerfile and pushes to a registry;
* builds a non-container binary and stores it in the Argo Workflows artifact repository;

It does not pretend to be a definitive example, but it aims to inspire.
In order to make this a semi-usable example, we have cut a number of security corners. Please don't just blindly run this in production.

## Prerequisites
### Running Locally
In order to run this locally, you will need [k3d](https://k3d.io/) installed, as well as kubectl.
```
chmod +x setup.sh
./setup.sh
```

### Running on a remote cluster
You will need kubectl installed locally, with the appropriate configuration to allow you access to the cluster.
## Running
### Running Locally

### Running on a remote cluster
You will need to use an empty cluster that you don't care about. This script blindly installs and configures a number of tools and has no regard for what you already have installed. If you're at all not sure, we recommend you use a local cluster instead.



# Running in production
This is a very simplified workflow aiming to highlight what's possible using Argo Workflows. Some things to consider when running in production:

* Triggering the CI using Argo Events. We have include an example of how to do this in the [TODO.md](TODO.md) file.
* Storing secrets more sensibly and injecting them only when required. We use Hashicorp Vault to achieve this. We strongly advise against putting any secret into git.
* Leveraging things like AWS spot instances and the cluster autoscaler to keep node costs down.
* Using much more restrictive Argo CD and Argo Workflows RBAC policies.
* Using something like the [ci-github-notifier](https://github.com/sendible-labs/ci-github-notifier) to annotate pull requests and branches with the status of your CI.
* Use dedicated images for the job. Don't pull alpine and install git on each run, use a custom alpine-git image. We just did the example this way to reduce the number of dependencies required to get up and running.
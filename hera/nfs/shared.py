from hera.workflows import *
from hera.workflows import models as m
from hera.exceptions import AlreadyExists
from hera.shared import global_config

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global_config.host = "https://localhost:8443/argo/"
global_config.token = "unused"
global_config.verify_ssl = False
global_config.namespace = 'argo'

from hera.shared import register_pre_build_hook

@register_pre_build_hook
def add_common_annotations_to_workflows(w: Workflow) -> Workflow:
    common_annotations = {
        'workflows.argoproj.io/maintainer': 'Pipekit Inc',
        'workflows.argoproj.io/maintainer_url': 'https://github.com/pipekit/argo-workflows-ci-example',
        'workflows.argoproj.io/version': '>= 3.5.2',
    }
    if w.annotations is None:
        w.annotations = common_annotations  # add common ones by default
    else:
        w.annotations |= common_annotations  # expand the user provided annotations with common ones
    return w

@register_pre_build_hook
def add_common_annotations_to_workflow_templates(w: WorkflowTemplate) -> WorkflowTemplate:
    common_annotations = {
        'workflows.argoproj.io/maintainer': 'Pipekit Inc',
        'workflows.argoproj.io/maintainer_url': 'https://github.com/pipekit/argo-workflows-ci-example',
        'workflows.argoproj.io/version': '>= 3.5.2',
    }
    if w.annotations is None:
        w.annotations = common_annotations  # add common ones by default
    else:
        w.annotations |= common_annotations  # expand the user provided annotations with common ones
    return w

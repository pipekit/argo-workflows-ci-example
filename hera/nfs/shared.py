from hera.shared import global_config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global_config.host = "https://localhost:8443/argo/"
global_config.token = "unused"
global_config.verify_ssl = False
namespace = 'argo'

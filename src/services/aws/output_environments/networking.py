from utils.project import *
from utils.aws_utils import *

# Fetch shared date information and base directory
date_info = get_current_date_info()
BASE_DIR = get_base_dir()
YEAR = date_info["year"]
MONTH = date_info["month"]
END_DATE = date_info["end_date"]


environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            # ELBv2 Files
            'elbv2_load_balancers': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-elbv2_load_balancers.json",
            'elbv2_listeners': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-elbv2_listeners.json",
            'elbv2_listener_rules': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-elbv2_target_groups.json",
            'elbv2_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-elbv2_tags.json",
            # WAFv2 Files
            'wafv2_web_acls': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-wafv2_web_acls.json",
            'wafv2_rules': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-wafv2_rules.json",
            'wafv2_ip_sets': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-wafv2_ip_sets.json",
            'wafv2_logging_config': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-wafv2_logging_config.json",
            'wafv2_tags': f"{BASE_DIR}/commercial/systems//aws/{YEAR}/{MONTH}/{END_DATE}-wafv2_tags.json",
            # App Mesh Files
            'meshes': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_meshes.json",
            'virtual_services': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_services.json",
            'virtual_routers': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_routers.json",
            'virtual_nodes': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_gateways.json",
            'routes': f"{BASE_DIR}/commercial/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_routes.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # ELBv2 Files
            'elbv2_load_balancers': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-elbv2_load_balancers.json",
            'elbv2_listeners': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-elbv2_listeners.json",
            'elbv2_listener_rules': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-elbv2_target_groups.json",
            'elbv2_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-elbv2_tags.json",
            # WAFv2 Files
            'wafv2_web_acls': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-wafv2_web_acls.json",
            'wafv2_rules': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-wafv2_rules.json",
            'wafv2_ip_sets': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-wafv2_ip_sets.json",
            'wafv2_logging_config': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-wafv2_logging_config.json",
            'wafv2_tags': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-wafv2_tags.json",
            # App Mesh Files
            'meshes': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_meshes.json",
            'virtual_services': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_services.json",
            'virtual_routers': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_routers.json",
            'virtual_nodes': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_virtual_gateways.json",
            'routes': f"{BASE_DIR}/federal/systems/aws/{config['region']}/{YEAR}/{MONTH}/{END_DATE}-appmesh_routes.json"
        }
    }
}

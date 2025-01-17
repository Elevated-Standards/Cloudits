# Purpose: Provide Evidence for AWS Network Related Services.#
##############################################################
import os
import subprocess
import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from credentials.aws import get_aws_credentials


YEAR = datetime.datetime.now().year
MONTH = datetime.datetime.now().strftime('%B')
DAY = datetime.datetime.now().day
START_DATE = (datetime.datetime.utcnow() - datetime.timedelta(days=31)).isoformat()  # 31 days ago
END_DATE = datetime.datetime.utcnow().isoformat()  # current time

# Environment configuration for AWS credentials and output paths
environments = {
    'commercial': {
        'region': 'us-east-1',
        'output_files': {
            # ELBv2 Files
            'elbv2_load_balancers': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_load_balancers.json",
            'elbv2_listeners': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listeners.json",
            'elbv2_listener_rules': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_target_groups.json",
            'elbv2_tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_tags.json",
            # WAFv2 Files
            'wafv2_web_acls': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_web_acls.json",
            'wafv2_rules': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_rules.json",
            'wafv2_ip_sets': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_ip_sets.json",
            'wafv2_logging_config': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_logging_config.json",
            'wafv2_tags': f"/evidence-artifacts/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_tags.json",
            # App Mesh Files
            'meshes': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_meshes.json",
            'virtual_services': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_services.json",
            'virtual_routers': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_routers.json",
            'virtual_nodes': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_gateways.json",
            'routes': f"/evidence-artifacts/commercial/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_routes.json"
        }
    },
    'federal': {
        'region': 'us-east-1',
        'output_files': {
            # ELBv2 Files
            'elbv2_load_balancers': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_load_balancers.json",
            'elbv2_listeners': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listeners.json",
            'elbv2_listener_rules': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_listener_rules.json",
            'elbv2_target_groups': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_target_groups.json",
            'elbv2_tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-elbv2_tags.json",
            # WAFv2 Files
            'wafv2_web_acls': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_web_acls.json",
            'wafv2_rules': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_rules.json",
            'wafv2_ip_sets': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_ip_sets.json",
            'wafv2_logging_config': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_logging_config.json",
            'wafv2_tags': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-wafv2_tags.json",
            # App Mesh Files
            'meshes': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_meshes.json",
            'virtual_services': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_services.json",
            'virtual_routers': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_routers.json",
            'virtual_nodes': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_nodes.json",
            'virtual_gateways': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_virtual_gateways.json",
            'routes': f"/evidence-artifacts/federal/systems/aws/{YEAR}/{MONTH}-{DAY}-appmesh_routes.json"
        }
    }
}

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(command)}\nError: {e}")
        return {}

# ELBv2 evidence collection functions
def fetch_load_balancers(config, output_file):
    load_balancers_data = run_command(['aws', 'elbv2', 'describe-load-balancers', '--region', config['region'], '--output', 'json'])
    fetch_and_save_data(command, output_file)
    with open(output_file, 'w') as f:
        json.dump(load_balancers_data, f, indent=4)

def fetch_listeners(config, output_file):
    """
    Fetch ELBv2 listeners for all load balancers and save to output file.
    """
    load_balancers_command = ['aws', 'elbv2', 'describe-load-balancers', '--region', config['region'], '--output', 'json']
    load_balancers_data = run_command(load_balancers_command)

    listeners_data = []
    for lb in load_balancers_data.get('LoadBalancers', []):
        lb_arn = lb['LoadBalancerArn']
        listeners_command = ['aws', 'elbv2', 'describe-listeners', '--load-balancer-arn', lb_arn, '--output', 'json']
        lb_listeners = run_command(listeners_command)
        listeners_data.extend(lb_listeners.get('Listeners', []))

    with open(output_file, 'w') as f:
        json.dump(listeners_data, f, indent=4)


def fetch_listener_rules(config, output_file):
    """
    Fetch listener rules for all ELBv2 listeners and save to output file.
    """
    load_balancers_command = ['aws', 'elbv2', 'describe-load-balancers', '--region', config['region'], '--output', 'json']
    load_balancers_data = run_command(load_balancers_command)

    listener_rules_data = []
    for lb in load_balancers_data.get('LoadBalancers', []):
        lb_arn = lb['LoadBalancerArn']
        listeners_command = ['aws', 'elbv2', 'describe-listeners', '--load-balancer-arn', lb_arn, '--output', 'json']
        listeners = run_command(listeners_command)
        for listener in listeners.get('Listeners', []):
            listener_arn = listener['ListenerArn']
            rules_command = ['aws', 'elbv2', 'describe-rules', '--listener-arn', listener_arn, '--output', 'json']
            rules = run_command(rules_command)
            listener_rules_data.extend(rules.get('Rules', []))

    with open(output_file, 'w') as f:
        json.dump(listener_rules_data, f, indent=4)


def fetch_target_groups(config, output_file):
    """
    Fetch ELBv2 target groups and detailed health checks, then save to output file.
    """
    command = ['aws', 'elbv2', 'describe-target-groups', '--region', config['region'], '--output', 'json']
    target_groups_data = run_command(command)

    detailed_target_groups_data = []
    for tg in target_groups_data.get('TargetGroups', []):
        tg_arn = tg['TargetGroupArn']
        tg_details_command = ['aws', 'elbv2', 'describe-target-health', '--target-group-arn', tg_arn, '--output', 'json']
        tg_details = run_command(tg_details_command)
        detailed_target_groups_data.append({
            'TargetGroup': tg,
            'TargetHealthDescriptions': tg_details.get('TargetHealthDescriptions', [])
        })

    with open(output_file, 'w') as f:
        json.dump(detailed_target_groups_data, f, indent=4)


def fetch_elbv2_tags(config, output_file):
    load_balancers_data = run_command(['aws', 'elbv2', 'describe-load-balancers', '--region', config['region'], '--output', 'json'])
    target_groups_data = run_command(['aws', 'elbv2', 'describe-target-groups', '--region', config['region'], '--output', 'json'])
    tags_data = []

    # Fetch tags for each load balancer
    for lb in load_balancers_data.get('LoadBalancers', []):
        lb_arn = lb['LoadBalancerArn']
        lb_tags = run_command(['aws', 'elbv2', 'describe-tags', '--resource-arns', lb_arn, '--output', 'json'])
        tags_data.append({'ResourceArn': lb_arn, 'Tags': lb_tags.get('TagDescriptions', [])})

    # Fetch tags for each target group
    for tg in target_groups_data.get('TargetGroups', []):
        tg_arn = tg['TargetGroupArn']
        tg_tags = run_command(['aws', 'elbv2', 'describe-tags', '--resource-arns', tg_arn, '--output', 'json'])
        tags_data.append({'ResourceArn': tg_arn, 'Tags': tg_tags.get('TagDescriptions', [])})

    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# WAFv2 evidence collection functions
def fetch_web_acls(config, output_file, scope='REGIONAL'):
    """
    Fetch Web ACLs for the specified scope (REGIONAL or CLOUDFRONT).
    """
    web_acls_data = run_command(['aws', 'wafv2', 'list-web-acls', '--scope', scope, '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(web_acls_data, f, indent=4)

def fetch_rules(config, output_file, scope='REGIONAL'):
    """
    Fetch Web ACL rules for the specified scope (REGIONAL or CLOUDFRONT).
    """
    web_acls_data = run_command(['aws', 'wafv2', 'list-web-acls', '--scope', scope, '--region', config['region'], '--output', 'json'])
    rules_data = []
    for acl in web_acls_data.get('WebACLs', []):
        acl_rules = run_command(['aws', 'wafv2', 'get-web-acl', '--scope', scope, '--region', config['region'], '--name', acl['Name'], '--id', acl['Id'], '--output', 'json'])
        rules_data.append(acl_rules)
    with open(output_file, 'w') as f:
        json.dump(rules_data, f, indent=4)

def fetch_ip_sets(config, output_file, scope='REGIONAL'):
    """
    Fetch IP sets for the specified scope (REGIONAL or CLOUDFRONT).
    """
    ip_sets_data = run_command(['aws', 'wafv2', 'list-ip-sets', '--scope', scope, '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(ip_sets_data, f, indent=4)

def fetch_logging_config(config, output_file, scope='REGIONAL'):
    """
    Fetch logging configurations for the specified scope (REGIONAL or CLOUDFRONT).
    """
    logging_config_data = run_command(['aws', 'wafv2', 'list-logging-configurations', '--scope', scope, '--region', config['region'], '--output', 'json'])
    with open(output_file, 'w') as f:
        json.dump(logging_config_data, f, indent=4)

def fetch_wafv2_tags(config, output_file, scope='REGIONAL'):
    """
    Fetch WAFv2 resource tags for the specified scope (REGIONAL or CLOUDFRONT).
    """
    web_acls_data = run_command(['aws', 'wafv2', 'list-web-acls', '--scope', scope, '--region', config['region'], '--output', 'json'])
    tags_data = []
    for acl in web_acls_data.get('WebACLs', []):
        acl_arn = acl['ARN']
        acl_tags = run_command(['aws', 'wafv2', 'list-tags-for-resource', '--resource-arn', acl_arn, '--region', config['region'], '--output', 'json'])
        tags_data.append({'ResourceArn': acl_arn, 'Tags': acl_tags.get('TagInfoForResource', {}).get('TagList', [])})
    with open(output_file, 'w') as f:
        json.dump(tags_data, f, indent=4)

# App Mesh evidence collection functions
def fetch_meshes(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    detailed_meshes_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        mesh_details = run_command(['aws', 'appmesh', 'describe-mesh', '--mesh-name', mesh_name, '--output', 'json'])
        detailed_meshes_data.append(mesh_details)
    with open(output_file, 'w') as f:
        json.dump(detailed_meshes_data, f, indent=4)

def fetch_virtual_services(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    virtual_services_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        services = run_command(['aws', 'appmesh', 'list-virtual-services', '--mesh-name', mesh_name, '--output', 'json'])
        for service in services['virtualServices']:
            service_name = service['virtualServiceName']
            service_details = run_command(['aws', 'appmesh', 'describe-virtual-service', '--mesh-name', mesh_name, '--virtual-service-name', service_name, '--output', 'json'])
            virtual_services_data.append(service_details)
    with open(output_file, 'w') as f:
        json.dump(virtual_services_data, f, indent=4)

def fetch_virtual_routers(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    virtual_routers_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        routers = run_command(['aws', 'appmesh', 'list-virtual-routers', '--mesh-name', mesh_name, '--output', 'json'])
        for router in routers['virtualRouters']:
            router_name = router['virtualRouterName']
            router_details = run_command(['aws', 'appmesh', 'describe-virtual-router', '--mesh-name', mesh_name, '--virtual-router-name', router_name, '--output', 'json'])
            virtual_routers_data.append(router_details)
    with open(output_file, 'w') as f:
        json.dump(virtual_routers_data, f, indent=4)

def fetch_virtual_nodes(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    virtual_nodes_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        nodes = run_command(['aws', 'appmesh', 'list-virtual-nodes', '--mesh-name', mesh_name, '--output', 'json'])
        for node in nodes['virtualNodes']:
            node_name = node['virtualNodeName']
            node_details = run_command(['aws', 'appmesh', 'describe-virtual-node', '--mesh-name', mesh_name, '--virtual-node-name', node_name, '--output', 'json'])
            virtual_nodes_data.append(node_details)
    with open(output_file, 'w') as f:
        json.dump(virtual_nodes_data, f, indent=4)

def fetch_virtual_gateways(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    virtual_gateways_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        gateways = run_command(['aws', 'appmesh', 'list-virtual-gateways', '--mesh-name', mesh_name, '--output', 'json'])
        for gateway in gateways['virtualGateways']:
            gateway_name = gateway['virtualGatewayName']
            gateway_details = run_command(['aws', 'appmesh', 'describe-virtual-gateway', '--mesh-name', mesh_name, '--virtual-gateway-name', gateway_name, '--output', 'json'])
            virtual_gateways_data.append(gateway_details)
    with open(output_file, 'w') as f:
        json.dump(virtual_gateways_data, f, indent=4)

def fetch_routes(config, output_file):
    meshes_data = run_command(['aws', 'appmesh', 'list-meshes', '--region', config['region'], '--output', 'json'])
    routes_data = []
    for mesh in meshes_data['meshes']:
        mesh_name = mesh['meshName']
        routers = run_command(['aws', 'appmesh', 'list-virtual-routers', '--mesh-name', mesh_name, '--output', 'json'])
        for router in routers['virtualRouters']:
            router_name = router['virtualRouterName']
            routes = run_command(['aws', 'appmesh', 'list-routes', '--mesh-name', mesh_name, '--virtual-router-name', router_name, '--output', 'json'])
            for route in routes['routes']:
                route_name = route['routeName']
                route_details = run_command(['aws', 'appmesh', 'describe-route', '--mesh-name', mesh_name, '--virtual-router-name', router_name, '--route-name', route_name, '--output', 'json'])
                routes_data.append(route_details)
    with open(output_file, 'w') as f:
        json.dump(routes_data, f, indent=4)

def fetch_and_save_data(command, output_file):
    """
    Executes an AWS CLI command, fetches the data, and writes it to the output file.

    Args:
        command (list): AWS CLI command as a list of strings.
        output_file (str): Path to the file where data will be saved.

    Returns:
        None
    """
    data = run_command(command)
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

# Main function to execute each evidence collection task for both environments
def main():
    for env_name, config in environments.items():
        # Fetch AWS credentials for the current environment
        aws_creds = get_aws_credentials(env_name)
        if not aws_creds:
            print(f"Skipping environment '{env_name}' due to credential issues.")
            continue
        
        # Set AWS environment variables for subprocess commands
        os.environ['AWS_ACCESS_KEY_ID'] = aws_creds['access_key']
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_creds['secret_key']
        os.environ['AWS_DEFAULT_REGION'] = aws_creds['region']

        # Ensure directories exist for output files
        for file_path in config['output_files'].values():
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        print(f"Starting evidence collection for environment '{env_name}'...")

        # Define tasks
        tasks = [
            (fetch_load_balancers, config, config['output_files']['elbv2_load_balancers']),
            (fetch_listeners, config, config['output_files']['elbv2_listeners']),
            (fetch_listener_rules, config, config['output_files']['elbv2_listener_rules']),
            (fetch_target_groups, config, config['output_files']['elbv2_target_groups']),
            (fetch_elbv2_tags, config, config['output_files']['elbv2_tags']),
            (fetch_meshes, config, config['output_files']['meshes']),
            (fetch_virtual_services, config, config['output_files']['virtual_services']),
            (fetch_virtual_routers, config, config['output_files']['virtual_routers']),
            (fetch_virtual_nodes, config, config['output_files']['virtual_nodes']),
            (fetch_virtual_gateways, config, config['output_files']['virtual_gateways']),
            (fetch_routes, config, config['output_files']['routes']),
        ]

        # Add WAFv2 tasks for both scopes
        for scope in ['REGIONAL', 'CLOUDFRONT']:
            tasks.extend([
                (fetch_web_acls, config, config['output_files']['wafv2_web_acls'], scope),
                (fetch_rules, config, config['output_files']['wafv2_rules'], scope),
                (fetch_ip_sets, config, config['output_files']['wafv2_ip_sets'], scope),
                (fetch_logging_config, config, config['output_files']['wafv2_logging_config'], scope),
                (fetch_wafv2_tags, config, config['output_files']['wafv2_tags'], scope),
            ])

        # Execute tasks in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers based on system resources
            futures = {executor.submit(task[0], *task[1:]): task[0].__name__ for task in tasks}

            for future in as_completed(futures):
                task_name = futures[future]
                try:
                    future.result()
                    print(f"Task '{task_name}' completed successfully.")
                except Exception as e:
                    print(f"Task '{task_name}' failed with error: {e}")

    print("AWS ELBv2, WAFv2, and App Mesh configuration evidence collection completed for both environments.")

# Execute main function
if __name__ == "__main__":
    main()

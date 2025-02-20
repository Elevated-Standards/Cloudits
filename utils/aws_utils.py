# filepath: /workspaces/Cloudits/utils/aws_utils.py
import boto3
import logging

logger = logging.getLogger(__name__)

def get_required_parameters(service, function, region, credentials, additional_filters=None):
    client = boto3.client(
        service,
        region_name=region,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    parameters = {}
    if additional_filters:
        parameters.update(additional_filters)


    try:
        # 🔹 Fetch required Queue URL for SQS
        if service == 'sqs' and function in ['get_queue_attributes', 'list_queue_tags']:
            response = client.list_queues()
            if 'QueueUrls' in response and response['QueueUrls']:
                return {'QueueUrl': response['QueueUrls'][0]}

        # 🔹 Fetch required Topic ARN for SNS
        elif service == 'sns' and function in ['get_topic_attributes', 'get_subscription_attributes']:
            response = client.list_topics()
            if 'Topics' in response and response['Topics']:
                return {'TopicArn': response['Topics'][0]['TopicArn']}

        # 🔹 Fetch required Secret ID for SecretsManager
        elif service == 'secretsmanager' and function == 'get_secret_value':
            response = client.list_secrets()
            if 'SecretList' in response and response['SecretList']:
                return {'SecretId': response['SecretList'][0]['Name']}

        # 🔹 Fetch required Bucket Name for S3
        elif service == 's3' and function in ['get_bucket_location', 'get_bucket_encryption', 'get_bucket_website', 'get_bucket_tagging']:
            response = client.list_buckets()
            if 'Buckets' in response and response['Buckets']:
                return {'Bucket': response['Buckets'][0]['Name']}

        # 🔹 Fetch required DB Instance Identifier for RDS
        elif service == 'rds' and function == 'describe_db_instances':
            response = client.describe_db_instances()
            if 'DBInstances' in response and response['DBInstances']:
                return {'DBInstanceIdentifier': response['DBInstances'][0]['DBInstanceIdentifier']}

        # 🔹 Fetch required Instance ID for EC2
        elif service == 'ec2' and function == 'describe_instances':
            response = client.describe_instances()
            if 'Reservations' in response and response['Reservations']:
                instances = response['Reservations'][0].get('Instances', [])
                if instances:
                    return {'InstanceIds': [instances[0]['InstanceId']]}

        # 🔹 Fetch required Key ID for KMS
        elif service == 'kms' and function == 'get_key_policy':
            response = client.list_keys()
            if 'Keys' in response and response['Keys']:
                return {'KeyId': response['Keys'][0]['KeyId']}

        # 🔹 Fetch required Cluster Name for EKS
        elif service == 'eks' and function in ['describe_cluster', 'list_nodegroups', 'describe_nodegroup', 'list_fargate_profiles', 'describe_fargate_profile']:
            response = client.list_clusters()
            if 'clusters' in response and response['clusters']:
                cluster_name = response['clusters'][0]
                if function == 'describe_cluster':
                    return {'name': cluster_name}
                elif function == 'list_nodegroups':
                    return {'clusterName': cluster_name}
                elif function == 'describe_nodegroup':
                    nodegroups_response = client.list_nodegroups(clusterName=cluster_name)
                    if 'nodegroups' in nodegroups_response and nodegroups_response['nodegroups']:
                        return {'clusterName': cluster_name, 'nodegroupName': nodegroups_response['nodegroups'][0]}
                elif function == 'list_fargate_profiles':
                    return {'clusterName': cluster_name}
                elif function == 'describe_fargate_profile':
                    fargate_profiles_response = client.list_fargate_profiles(clusterName=cluster_name)
                    if 'fargateProfileNames' in fargate_profiles_response and fargate_profiles_response['fargateProfileNames']:
                        return {'clusterName': cluster_name, 'fargateProfileName': fargate_profiles_response['fargateProfileNames'][0]}

        # 🔹 Fetch required Table Name for DynamoDB
        elif service == 'dynamodb' and function == 'describe_table':
            response = client.list_tables()
            if 'TableNames' in response and response['TableNames']:
                return {'TableName': response['TableNames'][0]}

        # 🔹 Fetch required Distribution ID for CloudFront
        elif service == 'cloudfront' and function in ['get_distribution_config', 'list_invalidations']:
            response = client.list_distributions()
            if 'DistributionList' in response and 'Items' in response['DistributionList']:
                return {'DistributionId': response['DistributionList']['Items'][0]['Id']}

        # 🔹 Fetch required Load Balancer ARN for ELBv2
        elif service == 'elbv2' and function in ['describe_listeners', 'describe_target_groups', 'describe_target_health']:
            response = client.describe_load_balancers()
            if 'LoadBalancers' in response and response['LoadBalancers']:
                return {'LoadBalancerArn': response['LoadBalancers'][0]['LoadBalancerArn']}

        # 🔹 Fetch required Rule Group ARN for WAFv2
        elif service == 'wafv2' and function == 'get_rule_group':
            response = client.list_rule_groups(Scope='REGIONAL')
            if 'RuleGroups' in response and response['RuleGroups']:
                return {'Id': response['RuleGroups'][0]['Id'], 'Scope': 'REGIONAL'}

        # 🔹 Fetch required API ID for API Gateway v2
        elif service == 'apigatewayv2' and function in ['get_routes', 'get_stages', 'get_deployments']:
            response = client.get_apis()
            if 'Items' in response and response['Items']:
                return {'ApiId': response['Items'][0]['ApiId']}

        # 🔹 Fetch required Web ACL Name for WAF
        elif service == 'waf' and function == 'get_web_acl':
            response = client.list_web_acls()
            if 'WebACLs' in response and response['WebACLs']:
                return {'Name': response['WebACLs'][0]['Name'], 'Scope': 'REGIONAL'}

        # 🔹 Fetch required Parameter Name for SSM
        elif service == 'ssm' and function == 'get_parameter':
            response = client.describe_parameters()
            if 'Parameters' in response and response['Parameters']:
                return {'Name': response['Parameters'][0]['Name']}

        # 🔹 Fetch required Insight ARN for Security Hub
        elif service == 'securityhub' and function == 'get_insight_results':
            response = client.list_insights()
            if 'InsightArns' in response and response['InsightArns']:
                return {'InsightArn': response['InsightArns'][0]}

        # 🔹 Fetch required Resource ARN for Macie
        elif service == 'macie2' and function == 'describe_classification_job':
            response = client.list_classification_jobs()
            if 'items' in response and response['items']:
                return {'jobId': response['items'][0]['jobId']}

        # 🔹 Fetch required Id for Route53 Traffic Policy Versions
        elif service == 'route53' and function == 'list_traffic_policy_versions':
            response = client.list_traffic_policies()
            if 'TrafficPolicies' in response and response['TrafficPolicies']:
                return {'Id': response['TrafficPolicies'][0]['Id']}

        # 🔹 Fetch required GroupName for Resource Groups
        elif service == 'resource-groups' and function == 'get_group':
            response = client.list_groups()
            if 'GroupIdentifiers' in response and response['GroupIdentifiers']:
                return {'GroupName': response['GroupIdentifiers'][0]['GroupName']}

        # 🔹 Fetch required ParameterGroupName for Redshift Describe Cluster Parameter Groups
        elif service == 'redshift' and function == 'describe_cluster_parameter_groups':
            response = client.describe_cluster_parameter_groups()
            if 'ParameterGroups' in response and response['ParameterGroups']:
                return {'ParameterGroupName': response['ParameterGroups'][0]['ParameterGroupName']}

        # 🔹 Fetch required ClusterSecurityGroupName for Redshift Describe Cluster Security Groups
        elif service == 'redshift' and function == 'describe_cluster_security_groups':
            response = client.describe_cluster_security_groups()
            if 'ClusterSecurityGroups' in response and response['ClusterSecurityGroups']:
                return {'ClusterSecurityGroupName': response['ClusterSecurityGroups'][0]['ClusterSecurityGroupName']}

        # 🔹 Fetch required DataShareArn for Redshift Describe Data Shares
            try:
                response = client.describe_clusters()
                if 'Clusters' in response and response['Clusters']:
                    cluster_identifier = response['Clusters'][0]['ClusterIdentifier']
                    data_share_response = client.describe_data_shares(ClusterIdentifier=cluster_identifier)
                    if 'DataShares' in data_share_response and data_share_response['DataShares']:
                        return {'DataShareArn': data_share_response['DataShares'][0]['DataShareArn']}
            except Exception as e:
                logger.warning(f"Could not fetch DataShareArn for redshift: {e}")
                return {}
                return {}
                return {}
        elif service == 'lightsail' and function == 'get_relational_database':
            response = client.get_relational_databases()
            if 'relationalDatabases' in response and response['relationalDatabases']:
                return {'relationalDatabaseName': response['relationalDatabases'][0]['name']}

        # 🔹 Fetch required FunctionName for Lambda Get Function
        elif service == 'lambda' and function == 'get_function':
            response = client.list_functions()
            if 'Functions' in response and response['Functions']:
                return {'FunctionName': response['Functions'][0]['FunctionName']}

        # 🔹 Fetch required workspaceId for Grafana Describe Workspace
        elif service == 'grafana' and function == 'describe_workspace':
            response = client.list_workspaces()
            if 'workspaces' in response and response['workspaces']:
                return {'workspaceId': response['workspaces'][0]['workspaceId']}

        # 🔹 Fetch required ResourceName for ElastiCache List Tags For Resource
        elif service == 'elasticache' and function == 'list_tags_for_resource':
            response = client.describe_cache_clusters()
            if 'CacheClusters' in response and response['CacheClusters']:
                return {'ResourceName': response['CacheClusters'][0]['CacheClusterArn']}

        # 🔹 Fetch required BackupArn for DynamoDB Describe Backup
        elif service == 'dynamodb' and function == 'describe_backup':
            response = client.list_backups()
            if 'BackupSummaries' in response and response['BackupSummaries']:
                return {'BackupArn': response['BackupSummaries'][0]['BackupArn']}

        # 🔹 Fetch required TableName for DynamoDB Describe Continuous Backups
        elif service == 'dynamodb' and function == 'describe_continuous_backups':
            response = client.list_tables()
            if 'TableNames' in response and response['TableNames']:
                return {'TableName': response['TableNames'][0]}

        # 🔹 Fetch required RuleGroupArn for Network Firewall Describe Rule Group
        elif service == 'network-firewall' and function == 'describe_rule_group':
            response = client.list_rule_groups()
            if 'RuleGroups' in response and response['RuleGroups']:
                return {'RuleGroupArn': response['RuleGroups'][0]['RuleGroupArn']}

        # 🔹 Fetch required restApiId for APIGateway Get Resources, Get Stages, Get Deployments
        elif service == 'apigateway' and function in ['get_resources', 'get_stages', 'get_deployments']:
            response = client.get_rest_apis()
            if 'items' in response and response['items']:
                return {'restApiId': response['items'][0]['id']}

        # 🔹 Fetch required DistributionId for CloudFront List Invalidations
        elif service == 'cloudfront' and function == 'list_invalidations':
            response = client.list_distributions()
            if 'DistributionList' in response and 'Items' in response['DistributionList']:
                return {'DistributionId': response['DistributionList']['Items'][0]['Id']}

        # 🔹 Fetch required meshName for AppMesh List Virtual Services, Describe Virtual Service
        elif service == 'appmesh' and function in ['list_virtual_services', 'describe_virtual_service']:
            response = client.list_meshes()
            if 'meshes' in response and response['meshes']:
                mesh_name = response['meshes'][0]['meshName']
                if function == 'list_virtual_services':
                    return {'meshName': mesh_name}
                elif function == 'describe_virtual_service':
                    virtual_services_response = client.list_virtual_services(meshName=mesh_name)
                    if 'virtualServices' in virtual_services_response and virtual_services_response['virtualServices']:
                        return {
                            'meshName': mesh_name,
                            'virtualServiceName': virtual_services_response['virtualServices'][0]['virtualServiceName']
                        }

        # 🔹 Fetch required meshName (and node/router/route details) for AppMesh additional calls
        elif service == 'appmesh' and function in [
            'list_virtual_nodes', 'describe_virtual_node',
            'list_virtual_routers', 'describe_virtual_router',
            'list_routes', 'describe_route'
        ]:
            response = client.list_meshes()
            if 'meshes' in response and response['meshes']:
                mesh_name = response['meshes'][0]['meshName']

                if function == 'list_virtual_nodes':
                    return {'meshName': mesh_name}

                elif function == 'describe_virtual_node':
                    v_nodes_resp = client.list_virtual_nodes(meshName=mesh_name)
                    if 'virtualNodes' in v_nodes_resp and v_nodes_resp['virtualNodes']:
                        return {
                            'meshName': mesh_name,
                            'virtualNodeName': v_nodes_resp['virtualNodes'][0]['virtualNodeName']
                        }

                elif function == 'list_virtual_routers':
                    return {'meshName': mesh_name}

                elif function == 'describe_virtual_router':
                    v_routers_resp = client.list_virtual_routers(meshName=mesh_name)
                    if 'virtualRouters' in v_routers_resp and v_routers_resp['virtualRouters']:
                        return {
                            'meshName': mesh_name,
                            'virtualRouterName': v_routers_resp['virtualRouters'][0]['virtualRouterName']
                        }

                elif function == 'list_routes':
                    v_routers_resp = client.list_virtual_routers(meshName=mesh_name)
                    if 'virtualRouters' in v_routers_resp and v_routers_resp['virtualRouters']:
                        router_name = v_routers_resp['virtualRouters'][0]['virtualRouterName']
                        return {
                            'meshName': mesh_name,
                            'virtualRouterName': router_name
                        }

                elif function == 'describe_route':
                    v_routers_resp = client.list_virtual_routers(meshName=mesh_name)
                    if 'virtualRouters' in v_routers_resp and v_routers_resp['virtualRouters']:
                        router_name = v_routers_resp['virtualRouters'][0]['virtualRouterName']
                        routes_resp = client.list_routes(meshName=mesh_name, virtualRouterName=router_name)
                        if 'routes' in routes_resp and routes_resp['routes']:
                            return {
                                'meshName': mesh_name,
                                'virtualRouterName': router_name,
                                'routeName': routes_resp['routes'][0]['routeName']
                            }

        # 🔹 Fetch required Name, Scope, Id for WAFv2 Get Web ACL
        elif service == 'wafv2' and function == 'get_web_acl':
            response = client.list_web_acls(Scope='REGIONAL')  # Assuming REGIONAL scope
            if 'WebACLs' in response and response['WebACLs']:
                web_acl = response['WebACLs'][0]
                return {'Name': web_acl['Name'], 'Scope': 'REGIONAL', 'Id': web_acl['Id']}

        # 🔹 Fetch required jobId for Macie2 Describe Classification Job
        elif service == 'macie2' and function == 'describe_classification_job':
            response = client.list_classification_jobs()
            if 'items' in response and response['items']:
                return {'jobId': response['items'][0]['jobId']}

        # 🔹 Fetch required ProtectionId for Shield Describe Protection
        elif service == 'shield' and function == 'describe_protection':
            response = client.list_protections()
            if 'Protections' in response and response['Protections']:
                return {'ProtectionId': response['Protections'][0]['Id']}

        # 🔹 Fetch required ResourceArn for Shield List Attacks
        elif service == 'shield' and function == 'list_attacks':
            protection_response = client.list_protections()
            if 'Protections' in protection_response and protection_response['Protections']:
                protection_id = protection_response['Protections'][0]['Id']
                return {'ResourceArn': f'arn:aws:shield::{region}:{credentials["AccountId"]}:protection/{protection_id}'}

        # 🔹 Fetch required NextMarker, Limit for WAF-Regional List Rules
        elif service == 'waf-regional' and function == 'list_rules':
            return {'NextMarker': '', 'Limit': 50}

        # 🔹 Fetch required NextMarker, Limit for WAF-Regional List IP Sets
        elif service == 'waf-regional' and function == 'list_ip_sets':
            return {'NextMarker': '', 'Limit': 50}

        # 🔹 Fetch required NextMarker, Limit for WAF List Rules
        elif service == 'waf' and function == 'list_rules':
            return {'NextMarker': '', 'Limit': 50}

        # 🔹 Fetch required Name, Scope, Id for WAF Get IP Set
        elif service == 'waf' and function == 'get_ip_set':
            response = client.list_ip_sets()
            if 'IPSets' in response and response['IPSets']:
                ip_set = response['IPSets'][0]
                return {
                    'Name': ip_set['Name'],
                    'Scope': 'REGIONAL',
                    'Id': ip_set['IPSetId']
                }

        # 🔹 Fetch required accounts, regions for SecurityLake List Log Sources
        elif service == 'securitylake' and function == 'list_log_sources':
            return {'accounts': [], 'regions': []}

    except boto3.exceptions.Boto3Error as e:
        logger.warning(f"Boto3 error occurred while fetching parameters for {service} - {function}: {e}")
    except botocore.exceptions.ClientError as e:
        logger.warning(f"Client error occurred while fetching parameters for {service} - {function}: {e}")
    except Exception as e:
        logger.warning(f"An unexpected error occurred while fetching parameters for {service} - {function}: {e}")
    return {}
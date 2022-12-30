origin = {
    'api_key': None,  # ORIGIN_REPO_API_KEY
    'endpoint': 'grpc+ssl://repository.portal.dev.spaceone.dev:443'  # ORIGIN_REPO_ENDPOINT (Required)
}

target = {
    'api_key': None,  # TARGET_REPO_API_KEY
    'endpoint': None  # TARGET_REPO_ENDPOINT (Required)
}

sync_resource_type = [
    'plugin',
    'schema',
    'policy'
]

sync_plugins = [
    # 'plugin-aws-cloud-service-inven-collector',
    # 'plugin-aws-ec2-inven-collector',
    # 'plugin-aws-phd-inven-collector',
    # 'plugin-aws-trusted-advisor-inven-collector',
    # 'plugin-azure-inven-collector',
    # 'plugin-google-cloud-inven-collector',
    # 'plugin-aws-cloudtrail-mon-datasource',
    # 'plugin-aws-cloudwatch-mon-datasource',
    # 'plugin-azure-activity-log-mon-datasource',
    # 'plugin-azure-monitor-mon-datasource',
    # 'plugin-google-stackdriver-mon-datasource'
]

sync_schemas = [
    # 'aws_access_key',
    # 'aws_assume_role',
    # 'google_oauth2_credentials'
]

sync_policies = [
    # 'policy-managed-domain-admin',
    # 'policy-managed-domain-viewer'
]

ORIGIN = {
    'API_KEY': None,  # ORIGIN_REPO_API_KEY
    'ENDPOINT': 'grpc+ssl://repository.portal.dev.spaceone.dev:443'  # ORIGIN_REPO_ENDPOINT (Required)
}

TARGET = {
    'API_KEY': None,  # TARGET_REPO_API_KEY
    'ENDPOINT': None  # TARGET_REPO_ENDPOINT (Required)
}

SYNC_RESOURCE_TYPE = [
    'plugin',
    'schema',
    'policy'
]

SYNC_PLUGIN = [
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

SYNC_SCHEMA = [
    # 'aws_access_key',
    # 'aws_assume_role',
    # 'google_oauth2_credentials'
]

SYNC_POLICY = [
    # 'policy-managed-domain-admin',
    # 'policy-managed-domain-viewer'
]

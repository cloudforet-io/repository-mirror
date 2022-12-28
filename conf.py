# repository name 변경
# file > os.env > conf 순으로 적용 하게 끔 설정

# YAML_PATH = '~/.spaceone/environments/config.yml'
#
# API_KEY = '<API_TOKEN>'
#
# ENDPOINT = {
#     'REPOSITORY': 'grpc+ssl://xxxxx.dev.spaceone.dev:443/v1',
# }

ORIGIN = {
    'API_KEY': None,    # ORIGIN_REPO_API_KEY
    'ENDPOINT': 'grpc+ssl://repository.portal.dev.spaceone.dev:443'   # ORIGIN_REPO_ENDPOINT (Required)
}

TARGET = {
    'API_KEY': None,   # TARGET_REPO_API_KEY
    'ENDPOINT': None   # TARGET_REPO_ENDPOINT (Required)
}

SYNC_RESOURCE_TYPE = [
    'plugin',
    'schema',
    'policy'
]

SYNC_PLUGINS = [
    'plugin-aws-cloud-service-inven-collector',
    'plugin-aws-ec2-inven-collector',
    'plugin-aws-phd-inven-collector',
    'plugin-aws-trusted-advisor-inven-collector',
    'plugin-azure-inven-collector',
    'plugin-google-cloud-inven-collector',
    'plugin-aws-cloudtrail-mon-datasource',
    'plugin-aws-cloudwatch-mon-datasource',
    'plugin-azure-activity-log-mon-datasource',
    'plugin-azure-monitor-mon-datasource',
    'plugin-google-stackdriver-mon-datasource'
]

SYNC_SCHEMA = [

]
SYNC_POLICY = []

# only를 실제 create, update할때 params에 명세
# update시 멱등성을 위해 어떤 필드가 업데이트 되는 지 config로 관리
# schema의 pk = name
# policy의 pk = policy_id
# plugin의 pk = marketplace는 image에서 Local에서는 plugin_id로
#

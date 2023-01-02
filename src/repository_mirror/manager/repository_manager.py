from repository_mirror.lib.spaceone_client import SpaceoneClient
from repository_mirror.manager.plugin_manager import PluginManager
from repository_mirror.manager.policy_manager import PolicyManager
from repository_mirror.manager.schema_manager import SchemaManager


class RepositoryManager(SpaceoneClient):
    def __init__(self, config):
        super().__init__(config)

    def get_repository_id(self, repository_type):
        repository_id = ''
        response = self.list_repositories_from_origin(params={})
        for repository_info in response.get('results', []):
            if repository_info['repository_type'] == repository_type:
                repository_id = repository_info['repository_id']
        return repository_id

    def list_repositories_from_origin(self, params=None):
        message = self.target_client().Repository.list(params or {}, metadata=self.get_metadata())
        return self.change_message(message)

    def delete_resources_to_local_repository(self):
        """method for testing"""

        repository_id = self.get_repository_id('local')
        params = {'repository_id': repository_id}

        schema_manager = SchemaManager({})
        # policy_manager = PolicyManager({})
        plugin_manager = PluginManager({})
        schemas = schema_manager.list_schemas_from_target(params=params)
        for schema in schemas:
            schema_manager.delete_schema_from_target(params={'name': schema['name']})

        # plugins = policy_manager.list_policies_from_target(params=params)
        # for policy in plugins:
        #     policy_manager.delete_policy_from_target(params={'policy_id': policy['policy_id']})

        plugins = plugin_manager.list_plugins_from_target(params=params)
        for plugin in plugins:
            plugin_manager.delete_plugin_from_target(params={'plugin_id': plugin['plugin_id']})


if __name__ == '__main__':
    # test of remove all resources in TARGET
    repository_mgr = RepositoryManager({})
    print(repository_mgr.get_repository_id('local'))
    repository_mgr.delete_resources_to_local_repository()

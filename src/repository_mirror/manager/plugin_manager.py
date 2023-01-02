from repository_mirror.lib.spaceone_client import SpaceoneClient


class PluginManager(SpaceoneClient):
    def __init__(self, config):
        super().__init__(config)

    def register_plugin_from_target(self, params):
        self.target_client().Plugin.register(params, metadata=self.get_metadata())

    def update_plugin_from_target(self, params):
        self.target_client().Plugin.update(params, metadata=self.get_metadata())

    def list_plugins_from_origin(self, params):
        message = self.origin_client().Plugin.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def list_plugins_from_target(self, params):
        message = self.target_client().Plugin.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def delete_plugin_from_target(self, params):
        self.target_client().Plugin.deregister(params, metadata=self.get_metadata())

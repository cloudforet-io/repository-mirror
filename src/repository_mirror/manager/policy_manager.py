from repository_mirror.lib.spaceone_client import SpaceoneClient


class PolicyManager(SpaceoneClient):
    def __init__(self, config):
        super().__init__(config)

    def create_policy_from_target(self, params):
        self.target_client().Policy.create(params, metadata=self.get_metadata())

    def update_policy_from_target(self, params):
        self.target_client().Policy.update(params, metadata=self.get_metadata())

    def list_policies_from_origin(self, params):
        message = self.origin_client().Policy.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def list_policies_from_target(self, params):
        message = self.target_client().Policy.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def delete_policy_from_target(self, params):
        self.target_client().Policy.delete(params, metadata=self.get_metadata())

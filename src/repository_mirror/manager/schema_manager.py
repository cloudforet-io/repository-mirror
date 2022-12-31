from repository_mirror.lib.spaceone_client import SpaceoneClient


class SchemaManager(SpaceoneClient):
    def __init__(self, config):
        super().__init__(config)

    def create_schema_from_target(self, params):
        self.target_client().Schema.create(params, metadata=self.get_metadata())

    def list_schemas_from_origin(self, params):
        message = self.origin_client().Schema.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def list_schemas_from_target(self, params):
        message = self.target_client().Schema.list(params, metadata=self.get_metadata())
        return self.change_message(message).get('results', [])

    def delete_schema_from_target(self, params):
        self.target_client().Schema.delete(params, metadata=self.get_metadata())


if __name__ == '__main__':
    a = SchemaManager({})
    params = {'repository_id': 'repo-f42c8b88ee2b'}
    print(a.list_schemas_from_origin(params))
    print(len(a.list_schemas_from_origin(params)))
    params = {'repository_id': 'repo-d9e115714edc'}
    print(a.list_schemas_from_target(params))
    print(len(a.list_schemas_from_target(params)))

    params = {'repository_id': 'repo-f42c8b88ee2b'}
    print(a.list_schemas_from_target(params))
    print(len(a.list_schemas_from_target(params)))

    a.create_schema_from_target({})

from data_managers.file_loader import FileLoader


class AnalyzeService(object):
    """
    We will use 'DAL' interface which FileLoader will implement if we will have to support
    in different data bases (e.g. other file types or SQL)
    """

    def __init__(self, data_manager: FileLoader):
        self.data_manager = data_manager

    def get_iac_resources(self):
        return self.data_manager.get_iac_resources()

    def get_cloud_resources(self):
        return self.data_manager.get_cloud_resources()

    def analyze_resource(self, cloud_resource_id: str):
        cloud_resource = self.get_cloud_resources().get(cloud_resource_id)
        if cloud_resource is None:
            raise Exception("cloud resource was not found")
        iac_resource = self.get_iac_resources().get(cloud_resource_id)
        if cloud_resource == iac_resource:
            return {'CloudResourceItem': cloud_resource, 'IacResourceItem': iac_resource, 'State': 'Match',
                    'ChangeLog': []}
        else:
            if iac_resource is None:
                return {'CloudResourceItem': cloud_resource, 'IacResourceItem': iac_resource, 'State': 'Missing',
                        'ChangeLog': []}
            else:
                return {'CloudResourceItem': cloud_resource, 'IacResourceItem': iac_resource, 'State': 'Modified',
                        'ChangeLog': generate_changelogs(cloud_resource, iac_resource)}


def generate_changelogs(cloud_resource, iac_resource, father_key=None):
    changelogs = []
    for key in cloud_resource.keys():
        if cloud_resource.get(key) != iac_resource.get(key):
            if type(cloud_resource[key]) == dict:
                mini_change = generate_changelogs(cloud_resource[key], iac_resource[key], key)
                changelogs.extend(mini_change)
            else:
                if father_key is not None and "." not in father_key:
                    father_key = f"{father_key}."
                    change_key = father_key + key
                else:
                    change_key = key
                change = {"KeyName": change_key, "CloudValue": cloud_resource.get(key),
                          "IacValue": iac_resource.get(key)}
                changelogs.append(change)
    return changelogs

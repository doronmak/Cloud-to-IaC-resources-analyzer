import json
from settings.config import IAC_RESOURCES_FILE, CLOUD_RESOURCES_FILE


class FileLoader(object):
    def __init__(self):
        self.cloud_resources = load_data(CLOUD_RESOURCES_FILE)
        self.iac_resources = load_data(IAC_RESOURCES_FILE)

    def get_cloud_resources(self):
        return self.cloud_resources

    def get_iac_resources(self):
        return self.iac_resources


def read_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def load_data(file_path):
    try:
        data_as_dict = {}
        data = read_file(file_path)
        for obj in data:
            data_as_dict[obj.get('id')] = obj
            data_as_dict[obj.get('id')].pop('id')
        return data_as_dict
    except Exception as e:
        if type(e) == FileNotFoundError:
            print([f"MSG: the requested file was not found", f"Exception MSG: {e.__str__()}"])
            exit()
        else:
            print([f"MSG: unexpected exception accord", f"Exception MSG: {e.__str__()}"])
